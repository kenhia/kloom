// Scene and reading colours in a real browser (korg 3495). Each viewport gets
// a fresh page and runs every check:
//
// - the scene pane and the reading wear their own palettes: Reading colours
//   set to Always light leaves a dark section's scene dark;
// - the old Palette setting (kloom.palette) is carried over on load: Mixed,
//   Dark and Light each to the two settings that replaced it;
// - the new rows work keyboard-only: the selects from the gear, Advanced
//   opened with Enter, each brightness slider moved to both ends with Home and
//   End, Esc closing onto the gear, and every choice remembered;
// - text and lines keep 4.5:1 against their background, read off the page's
//   own computed colours, at both ends of both sliders, on both panes;
// - the pop-up stays on screen with no sideways scroll, and a slider is never
//   under the 9rem a select is held to.
//
//   node create-tools/colours-check/colours_check.mjs [--url URL] [--viewports 1280x800,390x844]
//
// Exits 1 on any failure.
import { launch } from '../lib/browser.mjs';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(name);
	return i < 0 ? fallback : args[i + 1];
};
const url = opt('--url', process.env.KLOOM_URL || 'http://localhost:5415');
const viewports = opt('--viewports', '1280x800,390x844')
	.split(',')
	.map((v) => v.split('x').map(Number));
// A frame in a dark section (western-civ's Myth, the night palette).
const frame = opt('--frame', 'western-civ/prometheus');

function fail(message) {
	console.error(`colours_check: ${message}`);
	process.exit(2);
}

/** WCAG body text, as engine/colour.ts holds every palette to. */
const MIN_CONTRAST = 4.5;
const CONTROL_MIN_REM = 9;

function luminance([r, g, b]) {
	const f = (c) => ((c /= 255) <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
	return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}
function contrast(a, b) {
	const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
	return (hi + 0.05) / (lo + 0.05);
}

const browser = await launch(fail);
const failures = [];
let checks = 0;
function expect(ok, what) {
	checks++;
	if (!ok) failures.push(what);
}

async function run([width, height]) {
	const at = `${width}x${height}`;
	const context = await browser.newContext({
		viewport: { width, height },
		reducedMotion: 'reduce'
	});
	const page = await context.newPage();
	const load = async (storage = {}) => {
		await page.evaluate((s) => {
			localStorage.clear();
			for (const [k, v] of Object.entries(s)) localStorage.setItem(k, v);
		}, storage);
		await page.reload({ waitUntil: 'networkidle' });
		await page.waitForSelector('.spine .scene');
	};
	await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
	await page.waitForSelector('.spine .scene');

	/** A pane's palette as the browser computed it: each colour as [r, g, b], and its scheme. */
	const colours = (selector) =>
		page.evaluate((selector) => {
			const el = document.querySelector(selector);
			const cs = getComputedStyle(el);
			const rgb = (name) => {
				// A registered <color> computes to rgb(); paint a probe to be sure of it.
				const probe = document.createElement('span');
				probe.style.color = cs.getPropertyValue(name).trim();
				el.append(probe);
				const c = getComputedStyle(probe)
					.color.match(/\d+(\.\d+)?/g)
					.slice(0, 3)
					.map(Number);
				probe.remove();
				return c;
			};
			return {
				scheme: cs.colorScheme,
				background: rgb('--background'),
				ink: rgb('--ink'),
				muted: rgb('--muted'),
				accent: rgb('--accent'),
				line: rgb('--line')
			};
		}, selector);
	const scene = () => colours('#spine-pane');
	const reading = () => colours('.shell');
	const holds = (p, when) => {
		for (const key of ['ink', 'muted', 'accent', 'line']) {
			const r = contrast(p[key], p.background);
			expect(r >= MIN_CONTRAST, `${at} ${when}: ${key} is ${r.toFixed(2)}:1`);
		}
	};
	const value = (label) =>
		page.evaluate((label) => {
			const l = [...document.querySelectorAll('.shell .settings label')].find(
				(l) => l.textContent.trim() === label
			);
			const c = document.getElementById(l.htmlFor);
			return { value: c.value, text: c.getAttribute('aria-valuetext') };
		}, label);
	const focused = () =>
		page.evaluate(() => {
			const el = document.activeElement;
			const label = el?.id && document.querySelector(`label[for="${el.id}"]`);
			return label ? label.textContent.trim() : (el?.textContent?.trim().slice(0, 30) ?? '');
		});
	/** Tab until a control is focused; false when it never is. */
	const tabTo = async (name, limit = 30) => {
		for (let i = 0; i < limit; i++) {
			if ((await focused()) === name) return true;
			await page.keyboard.press('Tab');
		}
		return false;
	};

	// 1. Out of the box: by section, the reading the same as the scene.
	await load();
	const s0 = await scene();
	const r0 = await reading();
	expect(s0.scheme === 'dark', `${at}: Myth's scene is dark by section (${s0.scheme})`);
	expect(
		JSON.stringify(s0.background) === JSON.stringify(r0.background),
		`${at}: the reading is the scene's palette by default`
	);

	// 2. The old Palette setting, carried over.
	for (const [old, want] of [
		['mixed', ['section', 'same']],
		['dark', ['dark', 'dark']],
		['light', ['light', 'light']]
	]) {
		await load({ 'kloom.palette': old });
		const got = [(await value('Scene colours')).value, (await value('Reading colours')).value];
		expect(
			got.join() === want.join(),
			`${at}: Palette ${old} becomes Scene ${want[0]}, Reading ${want[1]} (got ${got})`
		);
		if (old === 'light')
			expect(
				(await scene()).scheme === 'light' && (await reading()).scheme === 'light',
				`${at}: Palette light still paints both panes light`
			);
	}

	// 3. Keyboard only, from the gear.
	await load();
	await page.locator('.shell .gear').focus();
	await page.keyboard.press('Enter');
	expect(await tabTo('Reading colours'), `${at}: Tab reaches Reading colours`);
	await page.keyboard.press('ArrowDown'); // Same as scene -> Always light
	expect(
		(await value('Reading colours')).value === 'light',
		`${at}: ArrowDown picks Always light (${(await value('Reading colours')).value})`
	);
	const s1 = await scene();
	const r1 = await reading();
	expect(
		s1.scheme === 'dark' && r1.scheme === 'light',
		`${at}: the scene stays dark while the reading turns light (${s1.scheme}, ${r1.scheme})`
	);

	expect(await tabTo('Advanced'), `${at}: Tab reaches Advanced`);
	expect(
		!(await page.locator('.shell .settings details.advanced').getAttribute('open')),
		`${at}: Advanced starts collapsed`
	);
	await page.keyboard.press('Enter');
	expect(
		(await page.locator('.shell .settings details.advanced').getAttribute('open')) !== null,
		`${at}: Enter opens Advanced`
	);

	for (const [label, pane, ends] of [
		['Light brightness', reading, ['6 steps dimmer', '1 step brighter']],
		['Dark brightness', scene, ['2 steps darker', '6 steps lighter']]
	]) {
		expect(await tabTo(label), `${at}: Tab reaches ${label}`);
		for (const [key, said] of [
			['Home', ends[0]],
			['End', ends[1]]
		]) {
			await page.keyboard.press(key);
			const v = await value(label);
			expect(v.text === said, `${at}: ${key} on ${label} says "${said}" (${v.text})`);
			holds(await pane(), `${label} at ${said}`);
		}
	}
	// Leave the light slider dimmed, to see it remembered.
	await page.keyboard.press('Shift+Tab');
	expect(
		(await focused()) === 'Light brightness',
		`${at}: Shift+Tab goes back to Light brightness`
	);
	await page.keyboard.press('Home');

	const box = await page.evaluate(() => {
		const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
		const panel = document.querySelector('.shell .settings .panel').getBoundingClientRect();
		return {
			rem,
			sliders: [...document.querySelectorAll('.shell .settings input[type="range"]')].map(
				(s) => s.getBoundingClientRect().width
			),
			left: panel.left,
			right: panel.right,
			vw: document.documentElement.clientWidth,
			scroll: document.documentElement.scrollWidth
		};
	});
	for (const w of box.sliders)
		expect(
			w >= CONTROL_MIN_REM * box.rem - 0.5,
			`${at}: a slider is ${Math.round(w)}px, under ${CONTROL_MIN_REM}rem`
		);
	expect(box.left >= 0 && box.right <= box.vw, `${at}: the pop-up runs off screen`);
	expect(box.scroll <= box.vw, `${at}: the page scrolls sideways (${box.scroll} > ${box.vw})`);

	await page.keyboard.press('Escape');
	expect(
		await page.evaluate(() => document.activeElement?.matches('.gear')),
		`${at}: Esc closes the pop-up onto the gear`
	);
	const stored = await page.evaluate(() => [
		localStorage.getItem('kloom.reading'),
		localStorage.getItem('kloom.lightBrightness'),
		localStorage.getItem('kloom.darkBrightness')
	]);
	expect(stored.join() === 'light,-6,6', `${at}: the choices are remembered (${stored.join()})`);
	await page.reload({ waitUntil: 'networkidle' });
	await page.waitForSelector('.spine .scene');
	const r2 = await reading();
	expect(
		r2.scheme === 'light' && JSON.stringify(r2.background) !== JSON.stringify(r1.background),
		`${at}: after a reload the reading is still light, and dimmed`
	);
	holds(r2, 'the dimmed reading after a reload');

	await context.close();
}

for (const v of viewports) await run(v);
await browser.close();

for (const f of failures) console.log(`FAIL ${f}`);
console.log(
	`${checks - failures.length}/${checks} checks passed at ${viewports.map((v) => v.join('x')).join(', ')}`
);
process.exit(failures.length ? 1 : 0);
