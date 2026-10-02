// Ask eval, step 3 (korg 3483): the results as Markdown tables, for the sprint
// record. Reads answers.jsonl and grades.jsonl from --out.
//
//   node bench/ask-eval/report.mjs [--out .scratch/ask-eval]
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const i = process.argv.indexOf('--out');
const out = i > 0 ? process.argv[i + 1] : '.scratch/ask-eval';
const jsonl = (f) =>
	readFileSync(join(out, f), 'utf8')
		.split('\n')
		.filter(Boolean)
		.map((l) => JSON.parse(l));
const answers = jsonl('answers.jsonl').filter((a) => !a.error);
const grades = jsonl('grades.jsonl');
const conditions = [...new Set(answers.map((a) => a.condition))];

const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : NaN);
const pct = (xs, p) => {
	const s = [...xs].sort((a, b) => a - b);
	return s.length ? s[Math.min(s.length - 1, Math.floor(p * s.length))] : NaN;
};
const f1 = (n) => (Number.isFinite(n) ? n.toFixed(1) : '–');
const sec = (ms) => (Number.isFinite(ms) ? `${(ms / 1000).toFixed(1)} s` : '–');
const row = (cells) => `| ${cells.join(' | ')} |`;

const graded = (c) => grades.flatMap((g) => g.rows.filter((r) => r.condition === c));
const timed = (c) => answers.filter((a) => a.condition === c);

console.log(`Graded questions: ${grades.length}\n`);
console.log(
	row([
		'condition',
		'overall',
		'accuracy',
		'grounding',
		'honesty',
		'clarity',
		'with a false claim',
		'rule broken',
		'judged best',
		'words (median)'
	])
);
console.log(row(Array(10).fill('---')));
for (const c of conditions) {
	const g = graded(c);
	console.log(
		row([
			c,
			f1(mean(g.map((r) => r.overall))),
			f1(mean(g.map((r) => r.accuracy))),
			f1(mean(g.map((r) => r.grounding))),
			f1(mean(g.map((r) => r.honesty))),
			f1(mean(g.map((r) => r.clarity))),
			`${g.filter((r) => r.false_claims?.length).length} / ${g.length}`,
			`${g.filter((r) => r.mechanical.violations.length).length}`,
			`${grades.filter((x) => x.best === c).length}`,
			`${pct(
				g.map((r) => r.mechanical.words),
				0.5
			)}`
		])
	);
}

console.log('\nLatency (time to the first word of the answer, and to the end):\n');
console.log(
	row(['condition', 'first word, median', 'first word, p90', 'total, median', 'total, p90'])
);
console.log(row(Array(5).fill('---')));
const at = (t, key, p) => {
	const xs = t.map((a) => a[key]);
	return sec(pct(xs, p));
};
for (const c of conditions) {
	const t = timed(c);
	console.log(
		row([
			c,
			at(t, 'ttftMs', 0.5),
			at(t, 'ttftMs', 0.9),
			at(t, 'totalMs', 0.5),
			at(t, 'totalMs', 0.9)
		])
	);
}

const kinds = [...new Set(grades.map((g) => g.kind))];
console.log('\nOverall score by kind of question:\n');
console.log(row(['kind', ...conditions]));
console.log(row(Array(conditions.length + 1).fill('---')));
for (const k of kinds) {
	const gs = grades.filter((g) => g.kind === k);
	console.log(
		row([
			`${k} (${gs.length})`,
			...conditions.map((c) =>
				f1(mean(gs.flatMap((g) => g.rows.filter((r) => r.condition === c).map((r) => r.overall))))
			)
		])
	);
}

console.log('\nFalse claims and broken rules, by answer:\n');
for (const g of grades)
	for (const r of g.rows) {
		const notes = [...(r.false_claims ?? []), ...r.mechanical.violations];
		if (notes.length) console.log(`- ${g.id} ${r.condition}: ${notes.join('; ')}`);
	}

const busy = answers.filter(
	(a) => a.raBusyBefore && a.raBusyBefore.running + a.raBusyBefore.waiting > 0
);
console.log(`\nRA requests that found it busy with another consumer: ${busy.length}`);
const reasoning = answers.filter((a) => a.usage?.completion_tokens_details);
for (const c of conditions) {
	const r = reasoning.filter((a) => a.condition === c);
	if (r.length)
		console.log(
			`${c}: reasoning tokens median ${pct(
				r.map((a) => a.usage.completion_tokens_details.reasoning_tokens),
				0.5
			)}, max ${Math.max(...r.map((a) => a.usage.completion_tokens_details.reasoning_tokens))}; finish ≠ stop: ${r.filter((a) => a.finish !== 'stop').length}`
		);
}

// Web turns: how much searching, and whether the answer cites what it read.
for (const c of conditions) {
	const t = timed(c).filter((a) => a.tools || a.searches !== undefined);
	if (!t.length) continue;
	const calls = t.map((a) => (a.tools ? a.tools.length : a.searches));
	const cited = t.filter((a) => /^\s*[-*]?\s*\[W\d+\]\s+\S/m.test(a.text)).length;
	const fetched = t.filter((a) => a.tools?.some((x) => x.name === 'fetch')).length;
	console.log(
		`${c}: tool calls per answer median ${pct(calls, 0.5)}, max ${Math.max(...calls)}; ` +
			`answers listing a page ${cited} / ${t.length}` +
			(t[0].tools ? `; answers that read a page ${fetched} / ${t.length}` : '')
	);
}
