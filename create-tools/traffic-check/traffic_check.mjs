// The traffic page and the visit counter in a real browser (korg 3570).
//
// - a frame is counted as a visit, and opened, only after five seconds on
//   it: not after one, and not when the reader moves on first;
// - the grid's levels match readers seeded at 0, 1, 2, 3 and 5 (4+);
// - every trail's cells sit together, right after its anchor's cell;
// - the page fits 390px with no sideways scroll, in dark and in light;
// - an admin sees the start screen's Traffic link; once not an admin, the
//   link is gone and the page is a 404.
//
// It needs a server of its own on a data directory it seeded, whose dev
// reader is the admin (`just traffic-check` starts one):
//
//   node create-tools/traffic-check/traffic_check.mjs --url URL --data DIR --subjects DIR
//   node create-tools/traffic-check/traffic_check.mjs --seed DIR --admin LOGIN
//
// Exits 1 on any failure.
import { readdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { openAdmins } from '../../src/lib/server/admins.ts';
import { openReaderDb, openReaderStore } from '../../src/lib/server/sqlite-reader-store.ts';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(name);
	return i < 0 ? fallback : args[i + 1];
};

/** Readers per frame of western-civ, seeded before the server starts. */
const SEEDED = { prometheus: 1, writing: 2, 'printing-press': 3, alexander: 5 };
const LEVELS = { prometheus: 1, writing: 2, 'printing-press': 3, alexander: 4 };

const seedDir = opt('--seed');
if (seedDir) {
	const db = openReaderDb(join(resolve(seedDir), 'reader.db'));
	const store = openReaderStore(db);
	for (const [frame, n] of Object.entries(SEEDED))
		for (let r = 1; r <= n; r++)
			await store.frameVisit(`reader${r}@traffic.check`, 'western-civ', frame);
	openAdmins(db).enable(opt('--admin'));
	db.close();
	process.exit(0);
}

const { launch } = await import('../lib/browser.mjs');
const url = opt('--url', process.env.KLOOM_URL || 'http://localhost:5418');
const data = resolve(opt('--data', 'data'));
const subjects = resolve(opt('--subjects', 'subjects'));

function fail(message) {
	console.error(`traffic_check: ${message}`);
	process.exit(2);
}
const browser = await launch(fail);
const failures = [];
let checks = 0;
function expect(ok, what) {
	checks++;
	if (!ok) failures.push(what);
}

const db = new DatabaseSync(join(data, 'reader.db'));
const visits = (frame) =>
	db
		.prepare(
			`SELECT coalesce(sum(n), 0) AS n FROM frame_visit WHERE subject = 'western-civ' AND frame = ? AND reader NOT LIKE '%@traffic.check'`
		)
		.get(frame).n;
const seen = (frame) =>
	db
		.prepare(
			`SELECT count(*) AS n FROM seen WHERE subject = 'western-civ' AND frame = ? AND reader NOT LIKE '%@traffic.check'`
		)
		.get(frame).n;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const context = await browser.newContext({
	viewport: { width: 1280, height: 800 },
	reducedMotion: 'reduce'
});
const page = await context.newPage();

// 1. The dwell: a second is not a visit, a move on cancels one, five seconds is.
const spine = JSON.parse(readFileSync(join(subjects, 'western-civ', 'spine.json'), 'utf8'));
const main = spine.segments.flatMap((s) => s.frames);
const [stay, flick, next] = [
	'athenian-democracy',
	main[main.indexOf('athenian-democracy') + 1],
	main[main.indexOf('athenian-democracy') + 2]
];
await page.goto(`${url}/western-civ/${stay}`, { waitUntil: 'networkidle' });
await page.waitForSelector('.spine .scene');
await sleep(1500);
expect(visits(stay) === 0, `no visit to ${stay} after 1.5 s (${visits(stay)})`);
expect(seen(stay) === 0, `${stay} not opened after 1.5 s (${seen(stay)})`);
await sleep(4500);
expect(visits(stay) === 1, `one visit to ${stay} after 6 s (${visits(stay)})`);
expect(seen(stay) === 1, `${stay} opened after 6 s (${seen(stay)})`);
await page.goto(`${url}/western-civ/${flick}`, { waitUntil: 'networkidle' });
await page.waitForSelector('.spine .scene');
await sleep(1000);
await page.goto(`${url}/western-civ/${next}`, { waitUntil: 'networkidle' });
await page.waitForSelector('.spine .scene');
await sleep(6000);
expect(visits(flick) === 0, `no visit to ${flick}, left after 1 s (${visits(flick)})`);
expect(visits(next) === 1, `one visit to ${next} after 6 s (${visits(next)})`);

// 2. The grid: levels and trails.
const res = await page.goto(`${url}/admin/traffic`, { waitUntil: 'networkidle' });
expect(res?.status() === 200, `the admin gets the traffic page (${res?.status()})`);
const cells = await page.locator('[data-row] .cells a').evaluateAll((as) =>
	as.map((a) => ({
		row: a.closest('[data-row]').querySelector('h2').id.replace(/^row-/, ''),
		frame: a.dataset.frame,
		level: Number(a.dataset.level),
		trail: a.classList.contains('trail')
	}))
);
const civ = cells.filter((c) => c.row === 'western-civ');
const levelOf = (f) => civ.find((c) => c.frame === f)?.level;
for (const [frame, level] of Object.entries(LEVELS))
	expect(levelOf(frame) === level, `${frame} at level ${level} (${levelOf(frame)})`);
expect(levelOf(stay) === 1 && levelOf(next) === 1, `the frames visited here at level 1`);
const lit = new Set([...Object.keys(LEVELS), stay, next]);
expect(
	civ.every((c) => lit.has(c.frame) || c.level === 0),
	`every other frame at level 0 (${civ.filter((c) => !lit.has(c.frame) && c.level).map((c) => c.frame)})`
);
const at = new Map(civ.map((c, i) => [c.frame, i]));
for (const file of readdirSync(join(subjects, 'western-civ', 'trails'))) {
	const t = JSON.parse(readFileSync(join(subjects, 'western-civ', 'trails', file), 'utf8'));
	const ids = t.spine.segments.flatMap((s) => s.frames);
	const idx = ids.map((id) => at.get(id));
	const together = idx.every((i, k) => i === idx[0] + k);
	const back = civ.slice(0, idx[0]).findLastIndex((c) => !c.trail);
	expect(together && civ[idx[0]]?.trail, `${t.id}'s cells sit together, as trail cells`);
	expect(civ[back]?.frame === t.anchor, `${t.id}'s cells follow ${t.anchor} (${civ[back]?.frame})`);
}
// Keyboard: one tab stop per row, arrows move within it, Enter opens the frame.
await page.locator('[data-row="0"] a[tabindex="0"]').focus();
await page.keyboard.press('ArrowRight');
const focused = await page.evaluate(() => document.activeElement?.getAttribute('data-cell'));
expect(focused === '1', `ArrowRight moves to the row's next cell (${focused})`);
const readout = await page.locator('.readout').innerText();
expect(/reader/.test(readout), `the readout names the focused cell (${readout})`);

// 3. Phone width, dark and light.
for (const colorScheme of ['dark', 'light']) {
	const phone = await browser.newContext({ viewport: { width: 390, height: 844 }, colorScheme });
	const p = await phone.newPage();
	await p.goto(`${url}/admin/traffic`, { waitUntil: 'networkidle' });
	const [sw, iw] = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
	expect(sw <= iw, `no sideways scroll at 390px, ${colorScheme} (${sw} > ${iw})`);
	const bg = await p.evaluate(() => getComputedStyle(document.body).backgroundColor);
	expect(
		(colorScheme === 'light') === (bg !== 'rgb(11, 11, 13)'),
		`the ${colorScheme} page's own background (${bg})`
	);
	await p.screenshot({ path: join(data, `traffic-390-${colorScheme}.png`), fullPage: true });
	await phone.close();
}

// 4. The start screen's link, then not an admin: no link, and a 404.
await page.goto(`${url}/western-civ`, { waitUntil: 'networkidle' });
expect(
	(await page.locator('.start a', { hasText: 'Traffic' }).count()) === 1,
	'an admin sees Traffic on the start screen'
);
db.exec('DELETE FROM admin');
await page.reload({ waitUntil: 'networkidle' });
expect(
	(await page.locator('.start a', { hasText: 'Traffic' }).count()) === 0,
	'a reader who is not an admin does not'
);
const gone = await page.goto(`${url}/admin/traffic`, { waitUntil: 'networkidle' });
expect(
	gone?.status() === 404,
	`the page is a 404 to a reader who is not an admin (${gone?.status()})`
);

await browser.close();
db.close();
if (failures.length) {
	console.error(`traffic_check: ${failures.length} of ${checks} checks failed`);
	for (const f of failures) console.error(`  - ${f}`);
	process.exit(1);
}
console.log(`traffic_check: ${checks} checks passed`);
