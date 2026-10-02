// Ask eval, step 2 (korg 3483): grade every question's answers together, blind.
// The judge (Opus 5.5 through `claude -p`, the same headless invocation as the
// app's adapter) sees the frame exactly as the model did, the question, a note
// on what a good answer does, and the answers under shuffled letters. The
// rubric's shape follows kvllm's judged suite: 0-10 scores with a rationale,
// and mechanical checks that cap where a rule is objective.
//
//   node bench/ask-eval/judge.mjs [--out .scratch/ask-eval] [--ids q01]
//
// Resumable: a question already in grades.jsonl is skipped.
import { spawn } from 'node:child_process';
import { appendFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { runnerImport } from 'vite';

const arg = (name, fallback) => {
	const i = process.argv.indexOf(`--${name}`);
	return i > 0 ? process.argv[i + 1] : fallback;
};
const out = arg('out', '.scratch/ask-eval');
const ids = arg('ids', '').split(',').filter(Boolean);
const JUDGE_MODEL = 'claude-opus-5-5';

const load = async (p) => (await runnerImport(p, { configFile: false, logLevel: 'error' })).module;
const { askPrompt, citedNumbers } = await load('./engine/ai/prompt.ts');
const { askContext } = await load('./engine/ai/context.ts');
const { ContentDb } = await load('./engine/content-db.ts');
const db = ContentDb.open('data/content.db');

const JUDGE = `You grade answers given by AI models inside kloom, an interactive timeline for learning a subject. A reader looking at one frame asked a question; each model was given the frame's reading and its numbered sources (below, exactly as the model saw them) and these rules: ground the answer in the frame where it can, say clearly when it goes beyond the frame, mark a sentence drawn from a numbered source with [n] (material from the reading itself needs no marker), never invent a source, quotation or date, and answer in concise Markdown with no headings, under 250 words.

Some answers may have been allowed to search the web first. Those mark a sentence drawn from a web page with [W1], [W2], … and end with the pages used, one per line as "[W1] Page title — URL". You cannot open those pages: judge a [W] marker by whether the page it names plausibly says what the sentence says, and judge the facts as you would any others. Using the web is neither a merit nor a fault in itself; a better-informed answer is.

Grade each answer on its own, strictly and consistently, from 0 to 10 on four axes:
- accuracy: is what it says true, judged against the frame, its sources and well-established knowledge? A wrong date, name or mechanism costs heavily.
- grounding: do its [n] markers point at sources that support the sentence they sit on? A marker on the wrong source, or a number with no source, costs heavily. A sentence plainly drawn from a source but unmarked costs a little. An answer that needs no source and uses none scores 10.
- honesty: does it say when it does not know, or when it goes beyond the frame? Any invented name, date, quotation, figure or source caps this at 3.
- clarity: does it answer the question asked, plainly, at a sensible length and in the required format?

Then give one overall score (0-10) for how good an answer this is for the reader, and list any specific claims you believe are invented or false.

Reply with ONLY a JSON object, no code fence:
{"grades": {"<letter>": {"accuracy": n, "grounding": n, "honesty": n, "clarity": n, "overall": n, "false_claims": ["..."], "rationale": "<one or two sentences>"}}, "best": "<letter>"}`;

/** Mechanical checks: objective rules, applied before the judge's word. */
function mechanical(text, sourceCount) {
	const violations = [];
	// A web answer's closing page list is not part of the answer's length.
	const body = text.replace(/^\s*[-*]?\s*\[W\d+\].*$/gm, '');
	const words = body.trim().split(/\s+/).filter(Boolean).length;
	if (!text.trim()) violations.push('empty answer');
	if (words > 250) violations.push(`${words} words (limit 250)`);
	if (/^#{1,6}\s/m.test(text)) violations.push('uses a heading');
	if (/<\/?think>/i.test(text)) violations.push('reasoning leaked into the answer');
	const all = [...text.matchAll(/\[(\d+)\]/g)].map((m) => Number(m[1]));
	const outOfRange = all.filter((n) => n < 1 || n > sourceCount);
	if (outOfRange.length) violations.push(`markers with no source: ${[...new Set(outOfRange)]}`);
	return { words, markers: citedNumbers(text, sourceCount).length, violations };
}

function claude(system, prompt) {
	return new Promise((resolve, reject) => {
		const cwd = join(tmpdir(), 'kloom-ask');
		mkdirSync(cwd, { recursive: true });
		const child = spawn(
			'claude',
			[
				'-p',
				'--model',
				JUDGE_MODEL,
				'--output-format',
				'json',
				'--tools',
				'',
				'--strict-mcp-config',
				'--setting-sources',
				'',
				'--disable-slash-commands',
				'--no-session-persistence',
				'--system-prompt',
				system
			],
			{ cwd, stdio: ['pipe', 'pipe', 'pipe'] }
		);
		let stdout = '';
		child.stdout.on('data', (d) => (stdout += d));
		child.on('close', (code) => {
			try {
				const r = JSON.parse(stdout);
				if (r.is_error) reject(new Error(r.result));
				else resolve(r.result);
			} catch {
				reject(new Error(`judge exited ${code}: ${stdout.slice(0, 300)}`));
			}
		});
		child.stdin.end(prompt);
	});
}

/** A fixed shuffle per question, so a re-run grades under the same letters. */
function shuffled(items, seed) {
	let h = [...seed].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
	const a = [...items];
	for (let i = a.length - 1; i > 0; i--) {
		h = (h * 1103515245 + 12345) >>> 0;
		const j = h % (i + 1);
		[a[i], a[j]] = [a[j], a[i]];
	}
	return a;
}

const answers = readFileSync(join(out, 'answers.jsonl'), 'utf8')
	.split('\n')
	.filter(Boolean)
	.map((l) => JSON.parse(l))
	.filter((a) => !a.error);
const gradesPath = join(out, 'grades.jsonl');
const graded = new Set(
	existsSync(gradesPath)
		? readFileSync(gradesPath, 'utf8')
				.split('\n')
				.filter(Boolean)
				.map((l) => JSON.parse(l).id)
		: []
);

const { questions } = JSON.parse(readFileSync('bench/ask-eval/questions.json', 'utf8'));
for (const q of questions.filter((q) => !ids.length || ids.includes(q.id))) {
	if (graded.has(q.id)) continue;
	const mine = answers.filter((a) => a.id === q.id);
	if (!mine.length) continue;
	const head = db.head(q.subject);
	const context = askContext(head, q.frame, q.trail ?? null, db.source(q.subject, q.frame));
	const sourceCount = context.frame.citations.length;
	const letters = 'ABCDEFGH';
	const order = shuffled(mine, q.id);
	const prompt = [
		'=== What the model was given ===',
		askPrompt(context, q.question, false),
		'',
		...(q.expect ? ['=== Note for the grader ===', q.expect, ''] : []),
		'=== The answers ===',
		...order.flatMap((a, i) => [`--- Answer ${letters[i]} ---`, a.text.trim(), ''])
	].join('\n');
	let reply;
	for (let attempt = 0; attempt < 2 && !reply; attempt++) {
		try {
			const raw = await claude(JUDGE, prompt);
			reply = JSON.parse(raw.slice(raw.indexOf('{'), raw.lastIndexOf('}') + 1));
		} catch (e) {
			console.error(`${q.id}: ${e.message}`);
		}
	}
	if (!reply) continue;
	const rows = order.map((a, i) => ({
		condition: a.condition,
		letter: letters[i],
		...reply.grades[letters[i]],
		mechanical: mechanical(a.text, sourceCount)
	}));
	const best = order[letters.indexOf(reply.best)]?.condition ?? null;
	appendFileSync(gradesPath, `${JSON.stringify({ id: q.id, kind: q.kind, best, rows })}\n`);
	console.log(`${q.id} best ${best}: ${rows.map((r) => `${r.condition} ${r.overall}`).join(', ')}`);
}
db.close();
