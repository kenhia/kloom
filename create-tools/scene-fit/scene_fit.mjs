// Every frame's scene fits its row of the spine: nothing in the scene runs
// into the HUD above or below it, and the counter never overlaps the
// metadata (korg 3469). Loads each frame once in a headless Chromium and
// measures it at every viewport, with motion reduced so the layout is the
// one the staged entrance ends on.
//
//   node create-tools/scene-fit/scene_fit.mjs [--url URL] [--viewports 1280x800,…] [subject…]
//
// No subjects means every subject under subjects/. Exits 1 on any misfit.
// Uses the Playwright already on this machine rather than a dependency of the
// repo: $PLAYWRIGHT_CORE (a path to playwright-core's index.mjs) or the bun
// or npx cache, and $CHROME or ~/.cache/ms-playwright's Chromium.
import { existsSync, readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(name);
	if (i < 0) return fallback;
	const [value] = args.splice(i, 2).slice(1);
	return value;
};
const url = opt('--url', process.env.KLOOM_URL || 'http://localhost:5415');
const viewports = opt('--viewports', '1280x800,1400x900,390x844')
	.split(',')
	.map((v) => v.split('x').map(Number));
const subjects = args.length
	? args
	: readdirSync('subjects')
			.filter((d) => existsSync(join('subjects', d, 'subject.json')))
			.sort();

/** The newest match of each candidate pattern: dir/prefix*suffix. */
function newest(dir, prefix, suffix) {
	if (!existsSync(dir)) return [];
	return readdirSync(dir)
		.filter((n) => n.startsWith(prefix))
		.sort()
		.reverse()
		.map((n) => join(dir, n, suffix))
		.filter(existsSync);
}

function playwright() {
	const found = [
		process.env.PLAYWRIGHT_CORE,
		...newest(join(homedir(), '.bun/install/cache'), 'playwright-core@', 'index.mjs'),
		...newest(join(homedir(), '.npm/_npx'), '', 'node_modules/playwright-core/index.mjs')
	].filter(Boolean);
	if (!found.length) fail('no playwright-core found; set $PLAYWRIGHT_CORE to its index.mjs');
	return found[0];
}

function chrome() {
	const cache = join(homedir(), '.cache/ms-playwright');
	const found = [
		process.env.CHROME,
		...newest(cache, 'chromium-', 'chrome-linux64/chrome'),
		...newest(cache, 'chromium_headless_shell-', 'chrome-linux64/chrome-headless-shell')
	].filter(Boolean);
	if (!found.length) fail('no Chromium found; set $CHROME');
	return found[0];
}

function fail(message) {
	console.error(`scene_fit: ${message}`);
	process.exit(2);
}

/** Runs in the page: what in the scene does not fit, or an empty list. */
function measure() {
	const box = (el) => el?.getBoundingClientRect();
	const scene = document.querySelector('.spine .scene');
	const top = box(document.querySelector('.spine .hud.top'));
	const parts = [...document.querySelectorAll('.spine .hud.bottom > *')].map(box);
	if (!scene || !top || !parts.length) return ['no scene'];
	const floor = Math.min(...parts.map((r) => r.top));
	const misfits = [];
	for (const el of scene.children) {
		const r = box(el);
		const name = el.className.split(' ')[0];
		if (r.top < top.bottom - 1)
			misfits.push(`${name} into the top HUD by ${Math.round(top.bottom - r.top)}px`);
		if (r.bottom > floor + 1)
			misfits.push(`${name} into the bottom HUD by ${Math.round(r.bottom - floor)}px`);
	}
	const c = box(document.querySelector('.spine .counter'));
	const m = box(document.querySelector('.spine .metadata'));
	if (c && m) {
		const ox = Math.min(c.right, m.right) - Math.max(c.left, m.left);
		const oy = Math.min(c.bottom, m.bottom) - Math.max(c.top, m.top);
		if (ox > 0 && oy > 0) misfits.push(`counter over metadata ${Math.round(ox)}x${Math.round(oy)}`);
	}
	return misfits;
}

const { chromium } = await import(pathToFileURL(playwright()).href);
const browser = await chromium.launch({ executablePath: chrome() });
const context = await browser.newContext({ reducedMotion: 'reduce' });

const frames = subjects.flatMap((s) =>
	readdirSync(join('subjects', s, 'frames'))
		.sort()
		.map((f) => `${s}/${f}`)
);
const hits = [];

/** One frame at every viewport: its misfits, each prefixed with the size. */
async function check(page, frame) {
	const [w, h] = viewports[0];
	await page.setViewportSize({ width: w, height: h });
	await page.goto(`${url}/${frame}`, { waitUntil: 'domcontentloaded' });
	await page.waitForSelector('.spine .scene .headline, .spine .scene .dedication');
	await page.evaluate(() => document.fonts.ready);
	const found = [];
	for (const [width, height] of viewports) {
		await page.setViewportSize({ width, height });
		await page.evaluate(
			() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))
		);
		for (const m of await page.evaluate(measure)) found.push(`${width}x${height} ${frame}: ${m}`);
	}
	return found;
}

let next = 0;
async function worker() {
	const page = await context.newPage();
	while (next < frames.length) {
		const frame = frames[next++];
		// A dev server may reload the page mid-measure; try a frame three times.
		for (let tries = 1; ; tries++) {
			try {
				hits.push(...(await check(page, frame)));
				break;
			} catch (e) {
				if (tries === 3) throw new Error(`${frame}: ${e.message}`, { cause: e });
			}
		}
	}
	await page.close();
}
await Promise.all(Array.from({ length: 4 }, worker));
await browser.close();

hits.sort();
for (const h of hits) console.log(h);
const sizes = viewports.map((v) => v.join('x')).join(', ');
console.log(`${hits.length} misfits in ${frames.length} frames at ${sizes}`);
process.exit(hits.length ? 1 : 0);
