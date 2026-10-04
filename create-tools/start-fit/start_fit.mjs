// The start screen's layout in a real browser (korg 3514): the subject list
// and the big title can never meet, however many subjects there are.
//
// At 1024x768, 1280x800, 1400x900 and 390x844, with the library as served
// (today's ten subjects) and with 24 (the ten plus synthetic ones), for every
// subject's title in turn:
//
// - the title is one line and inside the viewport (or, below its 1.5rem
//   floor, wraps in two lines at most), and the tagline is not clipped;
// - from 60rem, the listbox is shown and the picker is not; below, the
//   reverse;
// - the title's box and the list's box (or the picker's) do not meet;
// - the list lies inside the dial's band;
// - after End and after Home the selected option is wholly in view, and the
//   carets say whether there is more above and below.
//
// The 24-subject library is built in a temporary directory: each real
// subject a directory of symlinks, each synthetic one its own subject.json
// (a new title) over a real subject's frames, spine and trails, so it
// compiles and every connection still resolves. It is served by a dev
// server this script starts and stops.
//
//   node create-tools/start-fit/start_fit.mjs [--url URL] [--only 10|24]
//
// Exits 1 on any failure.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, symlinkSync } from 'node:fs';
import { existsSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { launch } from '../lib/browser.mjs';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(name);
	return i < 0 ? fallback : args[i + 1];
};
const url = opt('--url', process.env.KLOOM_URL || 'http://localhost:5415');
const only = opt('--only', null);
const SIM_PORT = 5417;
const VIEWPORTS = [
	[1024, 768],
	[1280, 800],
	[1400, 900],
	[390, 844]
];
/** Long titles on purpose: the list's column and the title both meet them. */
const SIM_TITLES = [
	'The History of Astronomy',
	'Geology and the Deep Time of the Earth',
	'The Long Story of Medicine Before Germs',
	'Music',
	'The History of Writing Systems and the Printed Word',
	'Economics',
	'The Evolution of Flight',
	'Cartography: How We Drew the World',
	'Rivers',
	'The History of Agriculture and the Domestication of Plants',
	'Law',
	'Photography and the Moving Image',
	'The Sea',
	'The Industrial Revolution in Britain and Beyond'
];

function fail(message) {
	console.error(`start_fit: ${message}`);
	process.exit(2);
}

const failures = [];
let checks = 0;
function expect(ok, what) {
	checks++;
	if (!ok) failures.push(what);
}

/** The 24-subject library, in a temporary directory; returns its root. */
function simulatedLibrary() {
	const real = resolve('subjects');
	const ids = readdirSync(real, { withFileTypes: true })
		.filter((d) => d.isDirectory() && existsSync(join(real, d.name, 'subject.json')))
		.map((d) => d.name);
	const root = mkdtempSync(join(tmpdir(), 'kloom-start-fit-'));
	const subjects = join(root, 'subjects');
	mkdirSync(join(root, 'data'), { recursive: true });
	const parts = ['frames', 'spine.json', 'trails'];
	// The listing takes directories only, so a subject is a directory of links, never a link.
	for (const id of ids) {
		mkdirSync(join(subjects, id), { recursive: true });
		for (const part of [...parts, 'subject.json'])
			if (existsSync(join(real, id, part)))
				symlinkSync(join(real, id, part), join(subjects, id, part));
	}
	const base = ids[0];
	const manifest = JSON.parse(readFileSync(join(real, base, 'subject.json'), 'utf8'));
	SIM_TITLES.slice(0, 24 - ids.length).forEach((title, i) => {
		const dir = join(subjects, `zz-sim-${String(i).padStart(2, '0')}`);
		mkdirSync(dir);
		const own = { ...manifest, title };
		delete own.subtitle;
		writeFileSync(join(dir, 'subject.json'), JSON.stringify(own));
		for (const part of parts)
			if (existsSync(join(real, base, part))) symlinkSync(join(real, base, part), join(dir, part));
	});
	return { root, subjects, count: readdirSync(subjects).length };
}

/** A dev server over the simulated library; resolves once it answers. */
async function serve(lib) {
	const server = spawn(
		'node_modules/.bin/vite',
		['dev', '--host', '127.0.0.1', '--port', String(SIM_PORT), '--strictPort'],
		{
			env: {
				...process.env,
				KLOOM_SUBJECTS_DIR: lib.subjects,
				KLOOM_NAMES_DIR: resolve('names'),
				KLOOM_DATA_DIR: join(lib.root, 'data'),
				KLOOM_CONTENT_DB: join(lib.root, 'data', 'content.db')
			},
			stdio: 'ignore'
		}
	);
	const at = `http://127.0.0.1:${SIM_PORT}`;
	for (let i = 0; i < 120; i++) {
		if (server.exitCode !== null) fail(`the 24-subject dev server exited (${server.exitCode})`);
		const ok = await fetch(`${at}/`).then(
			(r) => r.ok,
			() => false
		);
		if (ok) return { at, server };
		await new Promise((r) => setTimeout(r, 500));
	}
	server.kill();
	fail('the 24-subject dev server did not answer');
}

const browser = await launch(fail);

/** Every check, at one viewport, against one served library. */
async function check(base, label, [width, height]) {
	const context = await browser.newContext({
		viewport: { width, height },
		reducedMotion: 'reduce'
	});
	const page = await context.newPage();
	const where = `${label} ${width}x${height}`;
	await page.goto(`${base}/`, { waitUntil: 'networkidle' });
	await page.waitForSelector('.start h2');
	const wide = width >= 960;
	const list = page.locator('.start [role="listbox"]');
	const picker = page.locator('.start select.picker');
	expect(
		(await list.isVisible()) === wide,
		`${where}: the listbox is ${wide ? 'shown' : 'hidden'}`
	);
	expect(
		(await picker.isVisible()) === !wide,
		`${where}: the picker is ${wide ? 'hidden' : 'shown'}`
	);

	const ids = await page.$$eval('.start select.picker option', (os) => os.map((o) => o.value));
	expect(ids.length > 1, `${where}: the subjects are listed (${ids.length})`);

	/** The title and the tagline, as they stand. */
	const measure = () =>
		page.evaluate(() => {
			const h2 = document.querySelector('.start h2');
			const range = document.createRange();
			range.selectNodeContents(h2);
			const lines = new Set([...range.getClientRects()].map((r) => Math.round(r.top))).size;
			const box = (el) => el && el.getBoundingClientRect().toJSON();
			const sub = document.querySelector('.start .subtitle');
			const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
			return {
				text: h2.textContent.trim(),
				lines,
				wrap: h2.classList.contains('wrap'),
				size: parseFloat(getComputedStyle(h2).fontSize),
				floor: 1.5 * rem,
				title: box(h2),
				titleClipped: h2.scrollWidth > h2.clientWidth + 1,
				sub: box(sub),
				subClipped: sub ? sub.scrollWidth > sub.clientWidth + 1 : false,
				list: box(document.querySelector('.start [role="listbox"]')),
				picker: box(document.querySelector('.start select.picker')),
				dial: box(document.querySelector('.start .dial'))
			};
		});
	const meets = (a, b) =>
		a &&
		b &&
		a.width &&
		b.width &&
		a.left < b.right &&
		b.left < a.right &&
		a.top < b.bottom &&
		b.top < a.bottom;

	for (const id of ids) {
		if (wide) {
			await page.$eval('.start [role="listbox"]', (l) => l.focus());
			// Select by keyboard: Home, then down to it.
			await page.keyboard.press('Home');
			for (let i = 0; i < ids.indexOf(id); i++) await page.keyboard.press('ArrowDown');
		} else await picker.selectOption(id);
		await page.waitForTimeout(30);
		const m = await measure();
		const at = `${where}, "${m.text}"`;
		expect(
			m.lines === 1 || (m.wrap && m.size <= m.floor + 0.5),
			`${at}: the title is one line (${m.lines} at ${m.size.toFixed(1)}px)`
		);
		expect(!m.wrap || m.lines <= 2, `${at}: a title below the floor wraps to two lines at most`);
		expect(
			m.title.left >= -1 && m.title.right <= width + 1 && !m.titleClipped,
			`${at}: the title is inside the viewport`
		);
		if (m.sub)
			expect(
				m.sub.left >= -1 && m.sub.right <= width + 1 && !m.subClipped,
				`${at}: the tagline is not clipped`
			);
		expect(!meets(m.title, wide ? m.list : m.picker), `${at}: the title and the list do not meet`);
		if (wide)
			expect(
				m.list.top >= m.dial.top - 1 && m.list.bottom <= m.dial.bottom + 1,
				`${at}: the list lies in the dial's band (${Math.round(m.list.top)}–${Math.round(m.list.bottom)} in ${Math.round(m.dial.top)}–${Math.round(m.dial.bottom)})`
			);
	}

	if (wide) {
		/** The selected option wholly in the list's view, and the carets as the scroll stands. */
		const view = () =>
			page.evaluate(() => {
				const list = document.querySelector('.start [role="listbox"]');
				const o = list.querySelector('[aria-selected="true"]').getBoundingClientRect();
				const l = list.getBoundingClientRect();
				const shown = (sel) => {
					const el = document.querySelector(sel);
					return !!el && !el.hidden && getComputedStyle(el).display !== 'none';
				};
				return {
					inView: o.top >= l.top - 1 && o.bottom <= l.bottom + 1,
					scrolls: list.scrollHeight > list.clientHeight + 1,
					atTop: list.scrollTop <= 1,
					atBottom: list.scrollTop >= list.scrollHeight - list.clientHeight - 1,
					up: shown('.start .caret.up'),
					down: shown('.start .caret.down')
				};
			});
		await page.$eval('.start [role="listbox"]', (l) => l.focus());
		for (const key of ['End', 'Home']) {
			await page.keyboard.press(key);
			await page.waitForTimeout(60);
			const v = await view();
			expect(v.inView, `${where}: after ${key}, the selected option is in view`);
			expect(
				v.up === (v.scrolls && !v.atTop) && v.down === (v.scrolls && !v.atBottom),
				`${where}: after ${key}, the carets match the scroll (up ${v.up}, down ${v.down}, top ${v.atTop}, bottom ${v.atBottom})`
			);
		}
		if (label === '24') {
			const v = await view();
			expect(v.scrolls, `${where}: 24 subjects scroll in the band`);
		}
	}
	await context.close();
}

const runs = [];
if (only !== '24') runs.push({ label: '10', base: url });
let sim = null;
let lib = null;
if (only !== '10') {
	lib = simulatedLibrary();
	if (lib.count !== 24) fail(`the simulated library has ${lib.count} subjects, not 24`);
	sim = await serve(lib);
	runs.push({ label: '24', base: sim.at });
}
try {
	for (const run of runs) for (const v of VIEWPORTS) await check(run.base, run.label, v);
} finally {
	await browser.close();
	sim?.server.kill();
	if (lib) rmSync(lib.root, { recursive: true, force: true });
}

for (const f of failures) console.log(`FAIL ${f}`);
console.log(`${checks - failures.length}/${checks} checks passed`);
process.exit(failures.length ? 1 : 0);
