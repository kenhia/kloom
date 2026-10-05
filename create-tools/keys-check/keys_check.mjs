// The settings pop-up and the keyboard shortcuts dialog in a real browser
// (korg 3493). Each viewport gets a fresh page and runs every check:
//
// - every select in the pop-up stays at or above its minimum width, even
//   with every label made very long, and the pop-up stays on screen;
// - the dialog works keyboard-only: open from the gear, the first row
//   focused, capture announced, Esc cancelling a capture without closing,
//   a reserved combination refused, a clash swapped, Esc closing with
//   focus back on the button;
// - the dialog fits the viewport, with no sideways scroll;
// - the help bar names a binding with a modifier, and it acts from outside
//   the panes;
// - a key stored in the old single-letter format still works.
//
//   node create-tools/keys-check/keys_check.mjs [--url URL] [--viewports 1280x800,390x844]
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
const frame = opt('--frame', 'western-civ/prometheus');

function fail(message) {
	console.error(`keys_check: ${message}`);
	process.exit(2);
}

/** The pop-up's selects' minimum, in rem: engine/ui/Settings.svelte. */
const SELECT_MIN_REM = 9;

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
	await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
	await page.waitForSelector('.spine .scene');
	await page.evaluate(() => localStorage.clear());
	await page.reload({ waitUntil: 'networkidle' });
	await page.waitForSelector('.spine .scene');

	const focused = () =>
		page.evaluate(() => {
			const el = document.activeElement;
			return el ? `${el.tagName.toLowerCase()} ${el.textContent?.trim().slice(0, 40)}` : '';
		});
	const said = () => page.locator('.keys-dialog .said').textContent();
	const row = (action) => page.locator(`.keys-dialog [data-row="${action}"] .binding`);

	// 1. The pop-up: open it from the gear by keyboard, then measure.
	await page.locator('.shell .gear').focus();
	await page.keyboard.press('Enter');
	const panel = page.locator('.shell .settings .panel');
	expect(await panel.isVisible(), `${at}: Enter on the gear opens the settings`);
	const measure = () =>
		page.evaluate(() => {
			const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
			const panel = document.querySelector('.shell .settings .panel').getBoundingClientRect();
			return {
				rem,
				selects: [...document.querySelectorAll('.shell .settings select')].map((s) => ({
					id: s.id,
					width: s.getBoundingClientRect().width
				})),
				left: panel.left,
				right: panel.right,
				vw: document.documentElement.clientWidth
			};
		});
	const fits = (m, when) => {
		for (const s of m.selects)
			expect(
				s.width >= SELECT_MIN_REM * m.rem - 0.5,
				`${at} ${when}: select ${s.id} is ${Math.round(s.width)}px, under ${SELECT_MIN_REM}rem`
			);
		expect(m.left >= 0 && m.right <= m.vw, `${at} ${when}: the pop-up runs off screen`);
	};
	fits(await measure(), 'as shipped');
	await page.evaluate(() => {
		for (const l of document.querySelectorAll('.shell .settings label'))
			l.textContent = `${l.textContent} with a label far longer than any setting has today`;
	});
	fits(await measure(), 'with long labels');

	// 2. The dialog, by keyboard alone.
	const opener = page.locator('.shell .settings button.keys');
	await opener.focus();
	await page.keyboard.press('Enter');
	const dialog = page.locator('.keys-dialog');
	expect(await dialog.isVisible(), `${at}: Enter on Keyboard shortcuts… opens the dialog`);
	expect(
		await page.evaluate(() => !!document.activeElement?.closest('[data-row="sync"] [data-change]')),
		`${at}: the dialog opens on the first row's Change (focus: ${await focused()})`
	);
	const fitsDialog = await page.evaluate(() => {
		const d = document.querySelector('.keys-dialog');
		const r = d.getBoundingClientRect();
		return (
			r.left >= 0 &&
			r.right <= document.documentElement.clientWidth &&
			d.scrollWidth <= d.clientWidth
		);
	});
	expect(fitsDialog, `${at}: the dialog fits the viewport with no sideways scroll`);

	await page.keyboard.press('Enter');
	expect(
		(await said()) === 'Press the new keys for sync the narrative, or Escape to cancel.',
		`${at}: capture is announced (said: ${await said()})`
	);
	expect(
		(await page.locator('.keys-dialog .said').getAttribute('role')) === 'status',
		`${at}: the announcement is a live status`
	);
	await page.keyboard.press('Escape');
	expect(await dialog.isVisible(), `${at}: Esc while capturing leaves the dialog open`);
	expect((await said()).includes('not changed'), `${at}: Esc cancels the capture`);
	expect((await row('sync').textContent()).trim() === 'S', `${at}: a cancelled capture keeps S`);

	await page.keyboard.press('Enter');
	await page.keyboard.press('Control+t');
	expect(
		(await said()).includes('Ctrl+T belongs to the browser or the system (a new tab).'),
		`${at}: Ctrl+T is refused with its reason (said: ${await said()})`
	);
	await page.keyboard.press('Alt+y');
	expect(
		(await row('sync').textContent()).replace(/\s/g, '') === 'Alt+Y',
		`${at}: Alt+Y is captured for sync (row: ${await row('sync').textContent()})`
	);
	expect((await said()) === 'Sync the narrative is now Alt+Y.', `${at}: the change is said`);

	// A clash: give the map Alt+Y, and swap.
	await page.locator('.keys-dialog [data-row="map"] [data-change]').focus();
	await page.keyboard.press('Enter');
	await page.keyboard.press('Alt+y');
	expect(
		await page.evaluate(() => !!document.activeElement?.matches('[data-row="map"] [data-swap]')),
		`${at}: a clash offers Swap, focused (focus: ${await focused()})`
	);
	await page.keyboard.press('Enter');
	expect(
		(await row('map').textContent()).replace(/\s/g, '') === 'Alt+Y' &&
			(await row('sync').textContent()).trim() === 'M',
		`${at}: Swap gives the map Alt+Y and sync the map's M`
	);

	await page.keyboard.press('Escape');
	expect(!(await dialog.isVisible()), `${at}: Esc closes the dialog`);
	expect(
		await page.evaluate(() => document.activeElement?.matches('.settings button.keys')),
		`${at}: focus returns to Keyboard shortcuts… (focus: ${await focused()})`
	);
	const stored = await page.evaluate(() => [
		localStorage.getItem('kloom.key.map'),
		localStorage.getItem('kloom.key.sync')
	]);
	expect(
		stored[0] === 'alt+y' && stored[1] === 'm',
		`${at}: the bindings are remembered (${stored})`
	);
	await page.keyboard.press('Escape');
	expect(
		await page.evaluate(() => document.activeElement?.matches('.gear')),
		`${at}: Esc closes the pop-up onto the gear`
	);

	// 3. The help bar, and a modified binding acting from outside the panes.
	const hint = (await page.locator('#ai-hint').textContent()).replace(/\s+/g, ' ');
	expect(hint.includes('Alt+Y map'), `${at}: the help bar names Alt+Y (${hint})`);
	await page.keyboard.press('Alt+y');
	const map = page.locator('dialog.map');
	await map.waitFor({ state: 'visible', timeout: 3000 }).catch(() => {});
	expect(await map.isVisible(), `${at}: Alt+Y opens the map from the gear`);
	await page.keyboard.press('Escape');

	// 4. A key stored before modifiers.
	await page.evaluate(() => {
		localStorage.clear();
		localStorage.setItem('kloom.key.contents', 'k');
	});
	await page.reload({ waitUntil: 'networkidle' });
	await page.waitForSelector('.spine .scene');
	const migrated = (await page.locator('#ai-hint').textContent()).replace(/\s+/g, ' ');
	expect(migrated.includes('K contents'), `${at}: a stored letter still binds (${migrated})`);

	await context.close();
}

for (const v of viewports) await run(v);
await browser.close();

for (const f of failures) console.log(`FAIL ${f}`);
console.log(
	`${checks - failures.length}/${checks} checks passed at ${viewports.map((v) => v.join('x')).join(', ')}`
);
process.exit(failures.length ? 1 : 0);
