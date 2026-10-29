// Printing a frame (korg 3497, docs/design.md §Printing) in a real browser,
// with print media emulated:
// - the app's controls are left off: the HUD tools and index, the timeline,
//   the tab row, the controls above the reading, the AI pane, the dividers,
//   the hint line and the trail buttons;
// - the scene (headline, drawing, place, counter) and a small header with the
//   subject, the frame's title and its URL print;
// - the reading is not a scrolling box: it is as tall as what it holds;
// - a white page in dark ink in a dark and a light palette, the drawing in
//   dark ink, colour kept on images and charts, a chart's accent still a colour;
// - the citations print opened;
// - and the header prints only: on screen it is not there.
// Each case is also saved as a PDF in .scratch/print-check/ to look at.
//
//   node create-tools/print-check/print_check.mjs [--url URL]
//
// Exits 1 on any failure.
import { mkdirSync, readFileSync } from 'node:fs';
import { launch } from '../lib/browser.mjs';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(name);
	return i < 0 ? fallback : args[i + 1];
};
const url = opt('--url', process.env.KLOOM_URL || 'http://localhost:5415');
const out = '.scratch/print-check';

function fail(message) {
	console.error(`print_check: ${message}`);
	process.exit(2);
}

const browser = await launch(fail);
const failures = [];
let checks = 0;
function expect(ok, what) {
	checks++;
	if (!ok) failures.push(what);
}

// A chart and images (ai/compute), the longest reading (western-civ), and
// the frame the item was reported on (nursing).
const cases = [
	['ai/compute', 'dark'],
	['ai/compute', 'light'],
	['western-civ/beethoven-ninth', 'dark'],
	['nursing/sacred-twenty', 'light']
];

const HIDDEN = [
	'.spine .corner',
	'.spine .timeline',
	'.tab-row',
	'.narrative .controls',
	'.panes > .ai',
	'.panes > [role="separator"]',
	'.shell > .hint',
	'.narrative .trails'
];

mkdirSync(out, { recursive: true });
for (const [frame, mode] of cases) {
	const what = `${frame} (${mode})`;
	const context = await browser.newContext({
		viewport: { width: 1280, height: 800 },
		reducedMotion: 'reduce'
	});
	await context.addInitScript((m) => {
		localStorage.setItem('kloom.scene', m);
		localStorage.setItem('kloom.reading', m);
	}, mode);
	const page = await context.newPage();
	await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
	await page.waitForSelector('.narrative .body p');

	// On screen, the print header is not there.
	expect(!(await page.locator('.print-head').isVisible()), `${what}: print header shows on screen`);

	await page.emulateMedia({ media: 'print' });
	const r = await page.evaluate((hidden) => {
		const $ = (s) => document.querySelector(s);
		const shown = (s) => [...document.querySelectorAll(s)].some((e) => e.checkVisibility());
		const css = (e, p) => (e ? getComputedStyle(e).getPropertyValue(p) : '');
		const reading = $('.narrative .reading');
		const chartAccent = $('.narrative .chart .accent');
		const plate = $('.spine .illustration svg path, .spine .illustration svg line');
		return {
			leaked: hidden.filter(shown),
			scene: shown('.spine .headline, .spine .dedication') && shown('.spine .position'),
			head: $('.print-head')?.checkVisibility() ? $('.print-head').textContent : null,
			clipped: reading.scrollHeight - reading.clientHeight,
			overflow: css(reading, 'overflow-y'),
			page: [
				css(document.body, 'background-color'),
				css($('.shell'), 'background-color'),
				css($('.spine'), 'background-color')
			],
			ink: [css(reading, 'color'), css($('.spine .headline .accent'), 'color')].filter(Boolean),
			line: plate ? css($('.spine .illustration'), 'color') : null,
			drawn: plate ? css(plate, 'stroke-dashoffset') : null,
			figures: [...document.querySelectorAll('.narrative .body img, .narrative .chart svg')].map(
				(e) => css(e, 'print-color-adjust')
			),
			chartAccent: chartAccent ? css(chartAccent, 'color') : null,
			citations: shown('.narrative .citations li'),
			hasCitations: !!$('.narrative .citations li'),
			title: document.querySelector('#reading-title')?.textContent?.trim() ?? ''
		};
	}, HIDDEN);

	const dark = (rgb) => {
		const [r, g, b] = (rgb.match(/[\d.]+/g) ?? []).map(Number);
		return r + g + b < 3 * 90;
	};
	expect(!r.leaked.length, `${what}: app controls print: ${r.leaked.join(', ')}`);
	expect(r.scene, `${what}: the scene does not print`);
	expect(
		r.head && r.head.includes(`/${frame}`) && r.head.includes('·'),
		`${what}: print header missing or without subject, title and URL: ${r.head}`
	);
	expect(
		r.clipped <= 1 && r.overflow === 'visible',
		`${what}: reading is a scrolling box (${r.overflow}, ${r.clipped}px hidden)`
	);
	expect(
		r.page.every((c) => c === 'rgb(255, 255, 255)'),
		`${what}: page not white: ${r.page.join(' / ')}`
	);
	expect(r.ink.every(dark), `${what}: text not dark ink: ${r.ink.join(' / ')}`);
	if (r.line) {
		expect(dark(r.line), `${what}: the drawing is not dark ink: ${r.line}`);
		expect(parseFloat(r.drawn) === 0, `${what}: the drawing is not fully drawn: ${r.drawn}`);
	}
	expect(
		r.figures.every((v) => v === 'exact'),
		`${what}: a figure prints without its colour: ${r.figures.join(', ')}`
	);
	if (r.chartAccent)
		expect(!dark(r.chartAccent), `${what}: chart accent lost its colour: ${r.chartAccent}`);
	if (r.hasCitations) expect(r.citations, `${what}: citations print closed`);

	const file = `${out}/${frame.replace('/', '-')}-${mode}.pdf`;
	await page.pdf({ path: file, format: 'Letter', printBackground: false });
	const pages = (readFileSync(file, 'latin1').match(/\/Type\s*\/Page[^s]/g) ?? []).length;
	console.log(
		`${what}: ${pages} page(s), ${r.figures.length} figure(s)${r.chartAccent ? ', chart' : ''} → ${file}`
	);
	await context.close();
}

await browser.close();
if (failures.length) {
	console.error(`print_check: ${failures.length} of ${checks} failed`);
	for (const f of failures) console.error(`  - ${f}`);
	process.exit(1);
}
console.log(`print_check: ${checks} checks passed`);
