import { EventEmitter } from 'node:events';
import { PassThrough } from 'node:stream';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import type { ChildProcessWithoutNullStreams } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { ClaudeCliProvider, claudeArgs, growArgs, parseStreamLine } from './claude-cli';
import type { ProviderEvent } from './provider';
import { context } from './fixture';

const delta = (text: string) =>
	JSON.stringify({
		type: 'stream_event',
		event: { type: 'content_block_delta', delta: { type: 'text_delta', text } }
	});
const result = (text: string, isError = false) =>
	JSON.stringify({ type: 'result', subtype: 'success', is_error: isError, result: text });

/** A stand-in `claude` process that prints `lines`, then exits with `code`. */
function fakeClaude(lines: string[], code = 0, { hang = false } = {}) {
	const calls: { command: string; args: string[]; cwd: string; stdin: string }[] = [];
	const spawn = (command: string, args: string[], cwd: string) => {
		const child = new EventEmitter() as ChildProcessWithoutNullStreams & {
			exitCode: number | null;
		};
		const stdin = new PassThrough();
		const stdout = new PassThrough();
		const call = { command, args, cwd, stdin: '' };
		calls.push(call);
		stdin.on('data', (d) => (call.stdin += d));
		Object.assign(child, {
			stdin,
			stdout,
			stderr: new PassThrough(),
			exitCode: null,
			signalCode: null
		});
		const exit = (c: number | null, signal: string | null) => {
			if (child.exitCode !== null || child.signalCode !== null) return;
			Object.assign(child, { exitCode: c, signalCode: signal });
			stdout.end();
			setImmediate(() => child.emit('close', c));
		};
		child.kill = () => (exit(null, 'SIGTERM'), true);
		setImmediate(() => {
			for (const l of lines) stdout.write(`${l}\n`);
			if (!hang) exit(code, null);
		});
		return child;
	};
	return { spawn, calls };
}

const cwd = join(tmpdir(), 'kloom-ask-test');

async function collect(p: ClaudeCliProvider, signal?: AbortSignal) {
	const out: ProviderEvent[] = [];
	for await (const e of p.ask({ context, question: 'Why?', model: 'claude-sonnet-5', signal }))
		out.push(e);
	return out;
}

describe('the claude -p adapter', () => {
	it('offers no tools, loads no MCP or settings, keeps no session, and passes the model as its own argument', () => {
		const args = claudeArgs('claude-sonnet-5');
		expect(args[0]).toBe('-p');
		expect(args[args.indexOf('--model') + 1]).toBe('claude-sonnet-5');
		expect(args[args.indexOf('--tools') + 1]).toBe('');
		expect(args[args.indexOf('--setting-sources') + 1]).toBe('');
		expect(args).toContain('--strict-mcp-config');
		expect(args).toContain('--no-session-persistence');
		expect(args[args.indexOf('--output-format') + 1]).toBe('stream-json');
	});

	it('offers a web turn WebSearch and WebFetch, pre-approved, and nothing else', () => {
		const args = claudeArgs('claude-sonnet-5', true);
		expect(args[args.indexOf('--tools') + 1]).toBe('WebSearch,WebFetch');
		expect(args[args.indexOf('--allowedTools') + 1]).toBe('WebSearch,WebFetch');
		expect(args.filter((a) => a === '--tools')).toHaveLength(1);
		expect(args[args.indexOf('--system-prompt') + 1]).toContain('[W1]');
		expect(claudeArgs('claude-sonnet-5')).not.toContain('--allowedTools');
	});

	it('says searching when a tool starts, dropping the text before it', async () => {
		const tool = JSON.stringify({
			type: 'stream_event',
			event: { type: 'content_block_start', content_block: { type: 'tool_use', name: 'WebSearch' } }
		});
		expect(parseStreamLine(tool)).toEqual({ kind: 'tool', name: 'WebSearch' });
		const { spawn, calls } = fakeClaude([
			delta('Let me look.'),
			tool,
			tool,
			delta('Found [W1].'),
			result('Found [W1].')
		]);
		const out: ProviderEvent[] = [];
		for await (const e of new ClaudeCliProvider({ spawn, cwd }).ask({
			context,
			question: 'Why?',
			model: 'claude-sonnet-5',
			web: true
		}))
			out.push(e);
		expect(out).toEqual([
			{ type: 'text', text: 'Let me look.' },
			{ type: 'status', status: 'searching' },
			{ type: 'text', text: 'Found [W1].' }
		]);
		expect(calls[0].args).toContain('--allowedTools');
		expect(calls[0].stdin).toContain('You may search the web');
	});

	it('reads text deltas and the result from stream-json, and ignores the rest', () => {
		expect(parseStreamLine(delta('Hi'))).toEqual({ kind: 'text', text: 'Hi' });
		expect(parseStreamLine(result('Hi'))).toEqual({ kind: 'result', ok: true, text: 'Hi' });
		expect(parseStreamLine(result('bad', true))).toEqual({
			kind: 'result',
			ok: false,
			text: 'bad'
		});
		expect(parseStreamLine(JSON.stringify({ type: 'system', subtype: 'init' }))).toBeNull();
		expect(parseStreamLine('not json')).toBeNull();
	});

	it('streams the answer, with the prompt on stdin, in its own empty directory', async () => {
		const fake = fakeClaude([delta('Gutenberg '), delta('printed.'), result('Gutenberg printed.')]);
		const events = await collect(new ClaudeCliProvider({ spawn: fake.spawn, cwd }));
		expect(events).toEqual([
			{ type: 'text', text: 'Gutenberg ' },
			{ type: 'text', text: 'printed.' }
		]);
		expect(fake.calls[0].cwd).toBe(cwd);
		expect(fake.calls[0].stdin).toContain('--- Question ---\nWhy?');
	});

	it('falls back to the result text when nothing streamed', async () => {
		const fake = fakeClaude([result('Whole answer.')]);
		expect(await collect(new ClaudeCliProvider({ spawn: fake.spawn, cwd }))).toEqual([
			{ type: 'text', text: 'Whole answer.' }
		]);
	});

	it('reports an error result, such as an unknown model', async () => {
		const fake = fakeClaude([result('There is an issue with the selected model.', true)], 1);
		expect(await collect(new ClaudeCliProvider({ spawn: fake.spawn, cwd }))).toEqual([
			{ type: 'error', message: 'There is an issue with the selected model.' }
		]);
	});

	it('reports a process that exits without a result', async () => {
		const fake = fakeClaude([], 2);
		const events = await collect(new ClaudeCliProvider({ spawn: fake.spawn, cwd }));
		expect(events).toEqual([
			{ type: 'error', message: 'The model stopped unexpectedly (exit 2).' }
		]);
	});

	it('kills a turn that runs past the timeout', async () => {
		const fake = fakeClaude([delta('Slow')], 0, { hang: true });
		const events = await collect(new ClaudeCliProvider({ spawn: fake.spawn, cwd, timeoutMs: 30 }));
		expect(events.at(-1)).toEqual({ type: 'error', message: 'The model took longer than 0.03s.' });
	});

	it('stops quietly when the reader aborts', async () => {
		const fake = fakeClaude([delta('Part')], 0, { hang: true });
		const abort = new AbortController();
		setTimeout(() => abort.abort(), 20);
		const events = await collect(new ClaudeCliProvider({ spawn: fake.spawn, cwd }), abort.signal);
		expect(events).toEqual([{ type: 'text', text: 'Part' }]);
	});

	it('gives grow file tools that write only in its directory, and no shell', () => {
		const args = growArgs('claude-opus-5-5', 'INSTRUCTIONS');
		expect(args[args.indexOf('--tools') + 1]).toBe('Read,Write,Edit,Glob,Grep');
		expect(args[args.indexOf('--permission-mode') + 1]).toBe('acceptEdits');
		const denied = args.slice(
			args.indexOf('--disallowedTools') + 1,
			args.indexOf('--strict-mcp-config')
		);
		expect(denied).toEqual(['Read(~/**)', 'Edit(~/**)', 'Write(~/**)']);
		expect(args[args.indexOf('--system-prompt') + 1]).toBe('INSTRUCTIONS');
		expect(args.join(' ')).not.toMatch(/Bash|dangerously|--add-dir/);
		expect(args).not.toContain('--allowedTools');
		const web = growArgs('claude-opus-5-5', 'I', true);
		expect(web[web.indexOf('--tools') + 1]).toBe('Read,Write,Edit,Glob,Grep,WebSearch,WebFetch');
		expect(web[web.indexOf('--allowedTools') + 1]).toBe('WebSearch,WebFetch');
	});

	it('runs grow in the job directory, reporting what the model is doing', async () => {
		const assistant = (name: string) =>
			JSON.stringify({ type: 'assistant', message: { content: [{ type: 'tool_use', name }] } });
		const { spawn, calls } = fakeClaude([
			assistant('Read'),
			assistant('Glob'),
			assistant('WebFetch'),
			assistant('Write'),
			assistant('Edit'),
			result('Added a frame.')
		]);
		const out: ProviderEvent[] = [];
		for await (const e of new ClaudeCliProvider({ spawn, cwd }).grow({
			workDir: '/tmp/kloom-grow-x',
			instructions: 'I',
			prompt: 'Verb: frames',
			model: 'claude-opus-5-5',
			web: true,
			timeoutMs: 1000
		}))
			out.push(e);
		expect(out).toEqual([
			{ type: 'status', status: 'reading' },
			{ type: 'status', status: 'searching' },
			{ type: 'status', status: 'writing' },
			{ type: 'text', text: 'Added a frame.' }
		]);
		expect(calls[0].cwd).toBe('/tmp/kloom-grow-x');
		expect(calls[0].stdin).toBe('Verb: frames');
	});
});
