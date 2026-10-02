// Ask eval, step 1 (korg 3483): ask every question in questions.json under each
// condition, exactly as the ask route asks it (the library's frame, askContext,
// the shared askSystem/askPrompt, no web), and record the answer and its timing.
//
//   node bench/ask-eval/run.mjs [--only sonnet,ra-low,sonnet-web,ra-low-web] [--ids q01,q02] [--out .scratch/ask-eval]
//
// Resumable: a (question, condition) already in answers.jsonl is skipped. One
// request at a time, so the RA (shared with kmon, kyac) is never flooded.
import { appendFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { runnerImport } from 'vite';
import { runTool, TOOLS } from './wikipedia-tools.mjs';

const arg = (name, fallback) => {
	const i = process.argv.indexOf(`--${name}`);
	return i > 0 ? process.argv[i + 1] : fallback;
};
const out = arg('out', '.scratch/ask-eval');
const raUrl = process.env.KLOOM_RA_URL ?? 'http://localhost:8000/v1';
mkdirSync(out, { recursive: true });

const load = async (p) => (await runnerImport(p, { configFile: false, logLevel: 'error' })).module;
const { askSystem, askPrompt } = await load('./engine/ai/prompt.ts');
const { askContext } = await load('./engine/ai/context.ts');
const { ContentDb } = await load('./engine/content-db.ts');
const { ClaudeCliProvider } = await load('./engine/ai/claude-cli.ts');

const db = ContentDb.open('data/content.db');
if (!db) throw new Error('No data/content.db: run `just build-content` first.');

const raModel = await fetch(`${raUrl}/models`)
	.then((r) => r.json())
	.then((j) => j.data[0].id);

/**
 * The conditions: Sonnet 5 through the real adapter, the RA at three efforts.
 * Haiku 4.5, the config's fast model, is opt-in with --only, as is the
 * `-web` set, which may search: Claude with its own
 * WebSearch and WebFetch, as a reader's web turn gets them, and the RA with a
 * Wikipedia-only shim (./wikipedia-tools.mjs), since it has no search of its own.
 */
const CONDITIONS = {
	sonnet: { model: 'claude-sonnet-5', claude: true },
	'ra-medium': { model: raModel, kwargs: null }, // the served default
	'ra-low': { model: raModel, kwargs: { reasoning_effort: 'low' } },
	'ra-off': { model: raModel, kwargs: { enable_thinking: false } },
	'sonnet-web': { model: 'claude-sonnet-5', claude: true, web: true },
	haiku: { model: 'claude-haiku-4-5-20251001', claude: true },
	'haiku-web': { model: 'claude-haiku-4-5-20251001', claude: true, web: true },
	// claude -p turns extended thinking on for Haiku (not for Sonnet 5, which
	// decides for itself); these turn it off, which is most of Haiku's speed.
	'haiku-nothink': { model: 'claude-haiku-4-5-20251001', claude: true, thinking: false },
	'haiku-nothink-web': {
		model: 'claude-haiku-4-5-20251001',
		claude: true,
		thinking: false,
		web: true
	},
	'ra-low-web': { model: raModel, kwargs: { reasoning_effort: 'low' }, web: true }
};
const only = arg('only', 'sonnet,ra-medium,ra-low,ra-off').split(',');

const claude = new ClaudeCliProvider({ timeoutMs: 300_000, webTimeoutMs: 300_000 });
const claudeNoThinking = new ClaudeCliProvider({
	timeoutMs: 300_000,
	webTimeoutMs: 300_000,
	cwd: join(tmpdir(), 'kloom-ask'),
	spawn: (command, args, cwd) =>
		spawn(command, args, {
			cwd,
			stdio: ['pipe', 'pipe', 'pipe'],
			env: { ...process.env, MAX_THINKING_TOKENS: '0' }
		})
});

async function askClaude(context, question, model, web = false, thinking = true) {
	const t0 = performance.now();
	let ttft = null;
	let text = '';
	let error = null;
	let searches = 0;
	for await (const e of (thinking ? claude : claudeNoThinking).ask({
		context,
		question,
		model,
		web
	})) {
		if (e.type === 'text') {
			ttft ??= performance.now() - t0;
			text += e.text;
		} else if (e.type === 'status') {
			// As ask does: text before a search was thinking aloud.
			searches++;
			text = '';
			ttft = null;
		} else if (e.type === 'error') error = e.message;
	}
	return {
		text,
		error,
		ttftMs: ttft,
		totalMs: performance.now() - t0,
		...(web ? { searches } : {})
	};
}

/**
 * One RA answer: streamed chat completions, the answer text and reasoning kept
 * apart. With web, a tool call runs and the conversation goes round again;
 * text before a tool call is dropped, as ask drops it, so time to the first
 * word is measured on the turn the reader would see.
 */
async function askRa(context, question, model, kwargs, web = false) {
	const busy = await raLoad();
	const t0 = performance.now();
	const messages = [
		{ role: 'system', content: askSystem(web) },
		{ role: 'user', content: askPrompt(context, question, web) }
	];
	const usage = { prompt_tokens: 0, completion_tokens: 0, reasoning_tokens: 0 };
	const tools = [];
	let firstAny = null;
	let reasoningChars = 0;
	for (let round = 0; round < 10; round++) {
		const turn = await raTurn(messages, model, kwargs, web, t0);
		if (turn.error) return { text: '', error: turn.error, ttftMs: null, totalMs: 0 };
		firstAny ??= turn.firstAny;
		reasoningChars += turn.reasoning.length;
		if (turn.usage) {
			usage.prompt_tokens += turn.usage.prompt_tokens;
			usage.completion_tokens += turn.usage.completion_tokens;
			usage.reasoning_tokens += turn.usage.completion_tokens_details?.reasoning_tokens ?? 0;
		}
		if (!turn.toolCalls.length)
			return {
				text: turn.text,
				error: null,
				ttftMs: turn.ttft,
				firstTokenMs: firstAny,
				totalMs: performance.now() - t0,
				reasoningChars,
				usage: {
					...usage,
					completion_tokens_details: { reasoning_tokens: usage.reasoning_tokens }
				},
				finish: turn.finish,
				raBusyBefore: busy,
				...(web ? { tools } : {})
			};
		messages.push({ role: 'assistant', content: turn.text || null, tool_calls: turn.toolCalls });
		for (const call of turn.toolCalls) {
			const result = await runTool(call.function.name, call.function.arguments);
			tools.push({ name: call.function.name, args: call.function.arguments, chars: result.length });
			messages.push({ role: 'tool', tool_call_id: call.id, content: result });
		}
	}
	return {
		text: '',
		error: 'more than 10 tool rounds',
		ttftMs: null,
		totalMs: performance.now() - t0,
		tools
	};
}

async function raTurn(messages, model, kwargs, web, t0) {
	let ttft = null;
	let firstAny = null;
	let text = '';
	let reasoning = '';
	let usage = null;
	let finish = null;
	const calls = [];
	const res = await fetch(`${raUrl}/chat/completions`, {
		method: 'POST',
		headers: { 'content-type': 'application/json' },
		signal: AbortSignal.timeout(600_000),
		body: JSON.stringify({
			model,
			stream: true,
			stream_options: { include_usage: true },
			max_completion_tokens: 8192,
			messages,
			...(web ? { tools: TOOLS } : {}),
			...(kwargs ? { chat_template_kwargs: kwargs } : {})
		})
	});
	if (!res.ok) return { error: `${res.status} ${await res.text()}` };
	let buf = '';
	const decoder = new TextDecoder();
	for await (const chunk of res.body) {
		buf += decoder.decode(chunk, { stream: true });
		let nl;
		while ((nl = buf.indexOf('\n')) >= 0) {
			const line = buf.slice(0, nl).trim();
			buf = buf.slice(nl + 1);
			if (!line.startsWith('data:')) continue;
			const data = line.slice(5).trim();
			if (data === '[DONE]') continue;
			const j = JSON.parse(data);
			if (j.usage) usage = j.usage;
			const choice = j.choices?.[0];
			if (!choice) continue;
			finish = choice.finish_reason ?? finish;
			const d = choice.delta ?? {};
			const r = d.reasoning ?? d.reasoning_content;
			if (r) {
				firstAny ??= performance.now() - t0;
				reasoning += r;
			}
			if (d.content) {
				firstAny ??= performance.now() - t0;
				ttft ??= performance.now() - t0;
				text += d.content;
			}
			for (const tc of d.tool_calls ?? []) {
				const c = (calls[tc.index] ??= {
					id: '',
					type: 'function',
					function: { name: '', arguments: '' }
				});
				if (tc.id) c.id = tc.id;
				if (tc.function?.name) c.function.name += tc.function.name;
				if (tc.function?.arguments) c.function.arguments += tc.function.arguments;
			}
		}
	}
	return {
		text: text.trim(),
		ttft,
		firstAny,
		reasoning,
		usage,
		finish,
		toolCalls: calls.filter(Boolean)
	};
}

/** What else the RA was doing when a request went in (vLLM's own gauges). */
async function raLoad() {
	try {
		const m = await fetch(raUrl.replace(/\/v1$/, '/metrics')).then((r) => r.text());
		const g = (n) => Number(m.match(new RegExp(`^vllm:${n}\\{[^}]*\\} (\\S+)`, 'm'))?.[1] ?? 0);
		return { running: g('num_requests_running'), waiting: g('num_requests_waiting') };
	} catch {
		return null;
	}
}

const answersPath = join(out, 'answers.jsonl');
const done = new Set(
	existsSync(answersPath)
		? readFileSync(answersPath, 'utf8')
				.split('\n')
				.filter(Boolean)
				.map((l) => JSON.parse(l))
				.filter((a) => !a.error)
				.map((a) => `${a.id}/${a.condition}`)
		: []
);

const ids = arg('ids', '').split(',').filter(Boolean);
const { questions } = JSON.parse(readFileSync('bench/ask-eval/questions.json', 'utf8'));
for (const q of questions.filter((q) => !ids.length || ids.includes(q.id))) {
	const head = db.head(q.subject);
	const source = head && db.source(q.subject, q.frame);
	const context = source && askContext(head, q.frame, q.trail ?? null, source);
	if (!context) throw new Error(`${q.id}: no frame ${q.subject}/${q.frame}`);
	for (const condition of only) {
		if (done.has(`${q.id}/${condition}`)) continue;
		const c = CONDITIONS[condition];
		const r = c.claude
			? await askClaude(context, q.question, c.model, c.web, c.thinking ?? true)
			: await askRa(context, q.question, c.model, c.kwargs, c.web);
		const row = { id: q.id, condition, model: c.model, at: new Date().toISOString(), ...r };
		appendFileSync(answersPath, `${JSON.stringify(row)}\n`);
		console.log(
			`${q.id} ${condition.padEnd(9)} ttft ${((r.ttftMs ?? 0) / 1000).toFixed(1)}s total ${(r.totalMs / 1000).toFixed(1)}s ${r.error ? `ERROR ${r.error}` : `${r.text.split(/\s+/).length}w`}`
		);
	}
}
db.close();
