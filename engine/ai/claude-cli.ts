import { spawn as nodeSpawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { askPrompt, askSystem } from './prompt';
import type { AskRequest, GrowRequest, Provider, ProviderEvent, ProviderStatus } from './provider';

/**
 * The first provider adapter: headless `claude -p` on the host, under its
 * logged-in subscription (the karc precedent). How it is invoked is recorded
 * in docs/design.md §Ask.
 */

export interface ClaudeCliOptions {
	/** The executable; `claude` on PATH by default. */
	command?: string;
	/** A turn that runs longer is killed and reported as an error. */
	timeoutMs?: number;
	/** The same for a turn that may use the web; 180s by default. */
	webTimeoutMs?: number;
	/**
	 * The working directory: an empty one, so no project's CLAUDE.md or
	 * settings are picked up. Created if missing.
	 */
	cwd?: string;
	/** For tests. */
	spawn?: (command: string, args: string[], cwd: string) => ChildProcessWithoutNullStreams;
}

/** The only tools a web turn gets. Pages can carry prompt injection; with
 * these two the worst case is a wrong answer, never an action. */
export const WEB_TOOLS = 'WebSearch,WebFetch';

/**
 * The arguments for one ask turn. Ask needs no tools, so none are offered,
 * unless the turn may use the web, when WebSearch and WebFetch are offered and
 * pre-approved, and nothing else. No MCP server is loaded, no settings file or
 * skill applies, and the session is not kept. The model id has been checked
 * against the app config; it is also a separate argv entry, never shell text.
 */
export function claudeArgs(model: string, web = false): string[] {
	return [
		'-p',
		'--model',
		model,
		'--output-format',
		'stream-json',
		'--verbose',
		'--include-partial-messages',
		...(web ? ['--tools', WEB_TOOLS, '--allowedTools', WEB_TOOLS] : ['--tools', '']),
		'--strict-mcp-config',
		'--setting-sources',
		'',
		'--disable-slash-commands',
		'--no-session-persistence',
		'--system-prompt',
		askSystem(web)
	];
}

/** The file tools a grow job gets, inside its working directory only. */
export const GROW_TOOLS = 'Read,Write,Edit,Glob,Grep';

/**
 * The arguments for one grow turn. The job works on a copy of the subject in
 * its own directory, which must not be under the home directory:
 * `acceptEdits` lets Write and Edit act inside the working directory and
 * nowhere else (a write elsewhere needs a prompt, which headless means
 * refused), and the home directory is denied outright, reads included, so a
 * page read on the web cannot talk the model into reading a secret. There is
 * no shell, so no model-written code runs on the host. Measured on claude
 * 2.1.283 (docs/design.md §Grow).
 */
export function growArgs(model: string, instructions: string, web = false): string[] {
	return [
		'-p',
		'--model',
		model,
		'--output-format',
		'stream-json',
		'--verbose',
		'--tools',
		web ? `${GROW_TOOLS},${WEB_TOOLS}` : GROW_TOOLS,
		...(web ? ['--allowedTools', WEB_TOOLS] : []),
		'--permission-mode',
		'acceptEdits',
		'--disallowedTools',
		'Read(~/**)',
		'Edit(~/**)',
		'Write(~/**)',
		'--strict-mcp-config',
		'--setting-sources',
		'',
		'--disable-slash-commands',
		'--no-session-persistence',
		'--system-prompt',
		instructions
	];
}

/** What a grow job is doing, from the tool it just started. */
export function growStatus(tool: string): ProviderStatus {
	if (tool === 'WebSearch' || tool === 'WebFetch') return 'searching';
	if (tool === 'Write' || tool === 'Edit') return 'writing';
	return 'reading';
}

/** What one stream-json line means for the answer; null when it means nothing. */
export type StreamLine =
	| { kind: 'text'; text: string }
	| { kind: 'tool'; name: string }
	| { kind: 'result'; ok: boolean; text: string }
	| null;

export function parseStreamLine(line: string): StreamLine {
	let msg: Record<string, unknown>;
	try {
		msg = JSON.parse(line);
	} catch {
		return null;
	}
	if (msg.type === 'stream_event') {
		const event = msg.event as {
			type?: string;
			delta?: { type?: string; text?: string };
			content_block?: { type?: string; name?: string };
		};
		if (event?.type === 'content_block_delta' && event.delta?.type === 'text_delta')
			return { kind: 'text', text: event.delta.text ?? '' };
		const block = event?.content_block;
		if (event?.type === 'content_block_start' && /tool_use$/.test(block?.type ?? ''))
			return { kind: 'tool', name: String(block?.name ?? '') };
		return null;
	}
	// Without partial messages (grow), a tool shows up in the assistant message.
	if (msg.type === 'assistant') {
		const content = (msg.message as { content?: unknown })?.content;
		const tool = Array.isArray(content)
			? content.find((c) => /tool_use$/.test(String(c?.type)))
			: undefined;
		return tool ? { kind: 'tool', name: String(tool.name ?? '') } : null;
	}
	if (msg.type === 'result')
		return { kind: 'result', ok: msg.is_error !== true, text: String(msg.result ?? '') };
	return null;
}

const clip = (s: string, n = 300) => (s.length > n ? `${s.slice(0, n)}…` : s);

export class ClaudeCliProvider implements Provider {
	readonly name = 'claude-cli';
	readonly #command: string;
	readonly #timeoutMs: number;
	readonly #webTimeoutMs: number;
	readonly #cwd: string;
	readonly #spawn: NonNullable<ClaudeCliOptions['spawn']>;

	constructor(options: ClaudeCliOptions = {}) {
		this.#command = options.command ?? 'claude';
		this.#timeoutMs = options.timeoutMs ?? 120_000;
		this.#webTimeoutMs = options.webTimeoutMs ?? 180_000;
		this.#cwd = options.cwd ?? join(tmpdir(), 'kloom-ask');
		this.#spawn =
			options.spawn ??
			((command, args, cwd) => nodeSpawn(command, args, { cwd, stdio: ['pipe', 'pipe', 'pipe'] }));
	}

	async *ask({ context, question, model, web, signal }: AskRequest): AsyncIterable<ProviderEvent> {
		mkdirSync(this.#cwd, { recursive: true });
		yield* this.#run({
			args: claudeArgs(model, web),
			stdin: askPrompt(context, question, web),
			cwd: this.#cwd,
			timeoutMs: web ? this.#webTimeoutMs : this.#timeoutMs,
			signal,
			// Any tool in an ask is a web search; the answer restarts after it.
			status: () => 'searching',
			restartOnTool: true
		});
	}

	async *grow({
		workDir,
		instructions,
		prompt,
		model,
		web,
		timeoutMs,
		signal
	}: GrowRequest): AsyncIterable<ProviderEvent> {
		yield* this.#run({
			args: growArgs(model, instructions, web),
			stdin: prompt,
			cwd: workDir,
			timeoutMs,
			signal,
			status: growStatus,
			restartOnTool: false
		});
	}

	/**
	 * One `claude -p` process: the prompt on stdin, stream-json out. Text is
	 * yielded as it streams, a tool starting becomes a status, and the final
	 * result line decides success. Killed on timeout or abort.
	 */
	async *#run(o: {
		args: string[];
		stdin: string;
		cwd: string;
		timeoutMs: number;
		signal?: AbortSignal;
		status: (tool: string) => ProviderStatus;
		/** Ask: text before a tool was thinking aloud, so the answer restarts. */
		restartOnTool: boolean;
	}): AsyncIterable<ProviderEvent> {
		const { signal, timeoutMs } = o;
		if (signal?.aborted) return;

		let child: ChildProcessWithoutNullStreams;
		try {
			child = this.#spawn(this.#command, o.args, o.cwd);
		} catch (e) {
			yield { type: 'error', message: `Could not start the model: ${(e as Error).message}` };
			return;
		}

		let stopped: 'timeout' | 'abort' | null = null;
		const kill = (why: 'timeout' | 'abort') => {
			stopped ??= why;
			child.kill('SIGTERM');
		};
		const timer = setTimeout(() => kill('timeout'), timeoutMs);
		const onAbort = () => kill('abort');
		signal?.addEventListener('abort', onAbort, { once: true });

		let stderr = '';
		child.stderr.on('data', (d) => (stderr = (stderr + d).slice(-2000)));
		let spawnError: Error | null = null;
		child.on('error', (e) => (spawnError = e));
		const exited = new Promise<number | null>((resolve) => child.on('close', resolve));

		child.stdin.on('error', () => {});
		child.stdin.end(o.stdin);

		let streamed = false;
		let current: ProviderStatus | null = null;
		let result: { ok: boolean; text: string } | null = null;
		try {
			for await (const line of createInterface({ input: child.stdout })) {
				const parsed = parseStreamLine(line);
				if (parsed?.kind === 'text' && parsed.text) {
					streamed = true;
					current = null;
					yield { type: 'text', text: parsed.text };
				} else if (parsed?.kind === 'tool') {
					const status = o.status(parsed.name);
					if (status === current) continue;
					current = status;
					if (o.restartOnTool) streamed = false;
					yield { type: 'status', status };
				} else if (parsed?.kind === 'result') result = parsed;
			}
			const code = await exited;
			if (stopped === 'abort') return;
			if (stopped === 'timeout') {
				yield { type: 'error', message: `The model took longer than ${timeoutMs / 1000}s.` };
			} else if (spawnError) {
				yield {
					type: 'error',
					message: `Could not start the model: ${(spawnError as Error).message}`
				};
			} else if (result && !result.ok) {
				yield { type: 'error', message: clip(result.text || 'The model reported an error.') };
			} else if (!result) {
				console.error(`claude exited ${code} without a result: ${stderr}`);
				yield { type: 'error', message: `The model stopped unexpectedly (exit ${code}).` };
			} else if (!streamed && result.text) {
				yield { type: 'text', text: result.text };
			}
		} finally {
			clearTimeout(timer);
			signal?.removeEventListener('abort', onAbort);
			if (child.exitCode === null && child.signalCode === null) child.kill('SIGTERM');
		}
	}
}
