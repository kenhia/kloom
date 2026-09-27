import { spawn as nodeSpawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { askPrompt, ASK_SYSTEM } from './prompt';
import type { AskRequest, Provider, ProviderEvent } from './provider';

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
	/**
	 * The working directory: an empty one, so no project's CLAUDE.md or
	 * settings are picked up. Created if missing.
	 */
	cwd?: string;
	/** For tests. */
	spawn?: (command: string, args: string[], cwd: string) => ChildProcessWithoutNullStreams;
}

/**
 * The arguments for one ask turn. Ask needs no tools, so none are offered, no
 * MCP server is loaded, no settings file or skill applies, and the session is
 * not kept. The model id has been checked against the app config; it is also
 * a separate argv entry, never shell text.
 */
export function claudeArgs(model: string): string[] {
	return [
		'-p',
		'--model',
		model,
		'--output-format',
		'stream-json',
		'--verbose',
		'--include-partial-messages',
		'--tools',
		'',
		'--strict-mcp-config',
		'--setting-sources',
		'',
		'--disable-slash-commands',
		'--no-session-persistence',
		'--system-prompt',
		ASK_SYSTEM
	];
}

/** What one stream-json line means for the answer; null when it means nothing. */
export type StreamLine =
	{ kind: 'text'; text: string } | { kind: 'result'; ok: boolean; text: string } | null;

export function parseStreamLine(line: string): StreamLine {
	let msg: Record<string, unknown>;
	try {
		msg = JSON.parse(line);
	} catch {
		return null;
	}
	if (msg.type === 'stream_event') {
		const event = msg.event as { type?: string; delta?: { type?: string; text?: string } };
		if (event?.type === 'content_block_delta' && event.delta?.type === 'text_delta')
			return { kind: 'text', text: event.delta.text ?? '' };
		return null;
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
	readonly #cwd: string;
	readonly #spawn: NonNullable<ClaudeCliOptions['spawn']>;

	constructor(options: ClaudeCliOptions = {}) {
		this.#command = options.command ?? 'claude';
		this.#timeoutMs = options.timeoutMs ?? 120_000;
		this.#cwd = options.cwd ?? join(tmpdir(), 'kloom-ask');
		this.#spawn =
			options.spawn ??
			((command, args, cwd) => nodeSpawn(command, args, { cwd, stdio: ['pipe', 'pipe', 'pipe'] }));
	}

	async *ask({ context, question, model, signal }: AskRequest): AsyncIterable<ProviderEvent> {
		if (signal?.aborted) return;
		mkdirSync(this.#cwd, { recursive: true });

		let child: ChildProcessWithoutNullStreams;
		try {
			child = this.#spawn(this.#command, claudeArgs(model), this.#cwd);
		} catch (e) {
			yield { type: 'error', message: `Could not start the model: ${(e as Error).message}` };
			return;
		}

		let stopped: 'timeout' | 'abort' | null = null;
		const kill = (why: 'timeout' | 'abort') => {
			stopped ??= why;
			child.kill('SIGTERM');
		};
		const timer = setTimeout(() => kill('timeout'), this.#timeoutMs);
		const onAbort = () => kill('abort');
		signal?.addEventListener('abort', onAbort, { once: true });

		let stderr = '';
		child.stderr.on('data', (d) => (stderr = (stderr + d).slice(-2000)));
		let spawnError: Error | null = null;
		child.on('error', (e) => (spawnError = e));
		const exited = new Promise<number | null>((resolve) => child.on('close', resolve));

		child.stdin.on('error', () => {});
		child.stdin.end(askPrompt(context, question));

		let streamed = false;
		let result: { ok: boolean; text: string } | null = null;
		try {
			for await (const line of createInterface({ input: child.stdout })) {
				const parsed = parseStreamLine(line);
				if (parsed?.kind === 'text' && parsed.text) {
					streamed = true;
					yield { type: 'text', text: parsed.text };
				} else if (parsed?.kind === 'result') result = parsed;
			}
			const code = await exited;
			if (stopped === 'abort') return;
			if (stopped === 'timeout') {
				yield { type: 'error', message: `The model took longer than ${this.#timeoutMs / 1000}s.` };
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
