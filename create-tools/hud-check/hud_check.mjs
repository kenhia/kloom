// The HUD's tooltips and Zoom drawing in a real browser (korg 3540, 3539).
//
// Tooltips:
// - no HUD control carries a `title` (the browser's own waits ~2 s and is
//   heard twice beside the control's name);
// - every HUD icon, the Bookmarks list included, shows its tooltip on hover
//   within a second, not at once, and the next one along shows at once;
// - one shows on keyboard focus, and Esc hides it and does nothing else.
//
// Zoom drawing:
// - Z on the spine opens the drawing full-screen, Z again closes it, focus
//   back where it was; Z then Esc; the button and the × by mouse;
// - the drawing fills the screen in dark and light scenes, a labelled
//   diagram (ai/alexnet) included, and at phone size;
// - Z typed into the AI box types, and opens nothing;
// - a frame with no drawing (its drawing stripped from /api/frame) has the
//   button marked unavailable and Z does nothing.
//
// Pop-ups:
// - the contents and bookmarks panels stay in the window at every width from
//   700 to 1920 pixels, however many icons the HUD gains (korg 3552).
//
//   node create-tools/hud-check/hud_check.mjs [--url URL]
//
// Exits 1 on any failure.
import { launch } from '../lib/browser.mjs';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(name);
	return i < 0 ? fallback : args[i + 1];
};
const url = opt('--url', process.env.KLOOM_URL || 'http://localhost:5415');

function fail(message) {
	console.error(`hud_check: ${message}`);
	process.exit(2);
}

const browser = await launch(fail);
const failures = [];
let checks = 0;
function expect(ok, what) {
	checks++;
	if (!ok) failures.push(what);
}

async function open(page, frame) {
	await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
	await page.waitForSelector('.spine .scene');
}
const tip = (page) => page.locator('.kloom-tooltip');
const tipShown = (page) => tip(page).isVisible();
/** Milliseconds until the tooltip shows, or null when it never did within `limit`. */
async function untilTip(page, limit = 1500) {
	const t0 = Date.now();
	try {
		await tip(page).waitFor({ state: 'visible', timeout: limit });
		return Date.now() - t0;
	} catch {
		return null;
	}
}
const zoomOpen = (page) =>
	page.evaluate(() => !!document.querySelector('dialog.zoom')?.hasAttribute('open'));
const focused = (page) =>
	page.evaluate(() => {
		const a = document.activeElement;
		return a ? `${a.tagName.toLowerCase()}.${[...a.classList].join('.')}` : '';
	});

// ---- Tooltips --------------------------------------------------------------
{
	const context = await browser.newContext({
		viewport: { width: 1280, height: 800 },
		reducedMotion: 'reduce'
	});
	const page = await context.newPage();
	await open(page, 'western-civ/prometheus');
	const hud = page.locator('.spine .hud .corner button, .tab-row .corner button');

	const titled = await page.evaluate(() =>
		[...document.querySelectorAll('.spine .hud button, .tab-row .corner button')]
			.filter((b) => b.hasAttribute('title'))
			.map((b) => b.textContent.trim())
	);
	expect(titled.length === 0, `HUD controls with a native title: ${titled.join(', ')}`);

	const count = await hud.count();
	expect(count >= 7, `the HUD has its icons (${count})`);
	await page.mouse.move(640, 700);
	await page.waitForTimeout(800);
	let first = true;
	for (let i = 0; i < count; i++) {
		const b = hud.nth(i);
		if (!(await b.isVisible())) continue;
		const name = (await b.innerText()).trim() || (await b.getAttribute('aria-label')) || `#${i}`;
		await b.hover();
		const ms = await untilTip(page);
		expect(ms !== null, `hovering "${name}" shows a tooltip`);
		const text = ms === null ? '' : (await tip(page).innerText()).trim();
		expect(text.length > 0, `"${name}"'s tooltip says something`);
		if (first && ms !== null) {
			expect(
				ms >= 200 && ms <= 1000,
				`the first tooltip waits a moment, not two seconds (${ms} ms)`
			);
			first = false;
		} else if (ms !== null) {
			expect(ms <= 250, `the next tooltip along shows at once ("${name}", ${ms} ms)`);
		}
	}

	// The Bookmarks list button, which had no tooltip at all.
	const list = page.locator('.bookmarks button[aria-expanded]');
	await page.mouse.move(640, 700);
	await page.waitForTimeout(900);
	await list.hover();
	expect((await untilTip(page)) !== null, `the Bookmarks list button shows a tooltip`);
	const said = (
		await tip(page)
			.innerText()
			.catch(() => '')
	).trim();
	expect(/^Bookmarks \(\d+\)$/.test(said), `the Bookmarks tooltip says "Bookmarks (N)" (${said})`);
	expect(
		(await tip(page).getAttribute('aria-hidden')) === 'true',
		`the tooltip is hidden from assistive technology`
	);

	// Leaving hides it.
	await page.mouse.move(640, 700);
	await page.waitForTimeout(400);
	expect(!(await tipShown(page)), `the tooltip goes when the pointer leaves`);

	// Keyboard focus shows one; Esc hides it and does nothing else.
	await page.waitForTimeout(900);
	await page.keyboard.press('Shift');
	await page.locator('.spine .hud .corner .zoom-drawing').focus();
	expect((await untilTip(page)) !== null, `keyboard focus on Zoom drawing shows its tooltip`);
	expect(
		/^Zoom drawing \(Z\)$/.test((await tip(page).innerText()).trim()),
		`Zoom drawing's tooltip names Z`
	);
	const before = page.url();
	await page.keyboard.press('Escape');
	await page.waitForTimeout(100);
	expect(!(await tipShown(page)), `Esc hides the tooltip`);
	expect(
		(await focused(page)).includes('zoom-drawing') && page.url() === before,
		`Esc on a tooltip leaves focus and the page where they were (${await focused(page)})`
	);
	await context.close();
}

// ---- Zoom drawing ----------------------------------------------------------
for (const [mode, viewport] of [
	['dark', { width: 1280, height: 800 }],
	['light', { width: 1280, height: 800 }],
	['dark', { width: 390, height: 844 }]
]) {
	const at = `${mode}, ${viewport.width}×${viewport.height}`;
	const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
	await context.addInitScript((m) => localStorage.setItem('kloom.scene', m), mode);
	const page = await context.newPage();

	for (const frame of ['western-civ/prometheus', 'ai/alexnet']) {
		await open(page, frame);
		const slider = page.locator('.spine [role="slider"]');
		await slider.focus();
		await page.keyboard.press('z');
		expect(await zoomOpen(page), `Z opens the drawing (${frame}, ${at})`);
		const fit = await page.evaluate(() => {
			const d = document.querySelector('dialog.zoom');
			const svg = d?.querySelector('.stage svg');
			if (!d || !svg) return null;
			const r = svg.getBoundingClientRect();
			const shown = svg.querySelector('path');
			const css = getComputedStyle(d);
			return {
				w: r.width / innerWidth,
				h: r.height / innerHeight,
				inside:
					r.left >= 0 && r.top >= 0 && r.right <= innerWidth + 1 && r.bottom <= innerHeight + 1,
				text: svg.querySelectorAll('text').length,
				drawn: shown ? getComputedStyle(shown).strokeDashoffset : '',
				bg: css.backgroundColor,
				ink: css.color,
				label: d.getAttribute('aria-label')
			};
		});
		expect(!!fit, `the dialog holds the drawing (${frame}, ${at})`);
		if (fit) {
			expect(
				Math.max(fit.w, fit.h) > 0.8,
				`the drawing fills the screen (${frame}, ${at}: ${fit.w.toFixed(2)} × ${fit.h.toFixed(2)})`
			);
			expect(fit.inside, `the drawing stays on screen (${frame}, ${at})`);
			expect(
				fit.bg !== fit.ink,
				`the drawing is drawn in a colour apart from its backdrop (${frame}, ${at})`
			);
			expect(
				fit.drawn === '' || fit.drawn === '0px' || fit.drawn === '0',
				`the drawing shows whole, not drawing on (${frame}, ${at}: ${fit.drawn})`
			);
			expect(
				/^Drawing: ./.test(fit.label ?? ''),
				`the dialog is named for the drawing (${fit.label})`
			);
			if (frame === 'ai/alexnet')
				expect(fit.text > 0, `a labelled diagram keeps its labels (${at})`);
		}
		await page.keyboard.press('z');
		expect(!(await zoomOpen(page)), `Z closes it again (${frame}, ${at})`);
		expect(
			(await focused(page)).includes('slider') ||
				(await page.evaluate(() => document.activeElement?.getAttribute('role'))) === 'slider',
			`focus returns to the spine after Z (${frame}, ${at})`
		);
		await page.keyboard.press('z');
		await page.keyboard.press('Escape');
		expect(!(await zoomOpen(page)), `Esc closes it (${frame}, ${at})`);
		expect(
			(await page.evaluate(() => document.activeElement?.getAttribute('role'))) === 'slider',
			`focus returns to the spine after Esc (${frame}, ${at})`
		);
	}

	// By mouse: the button, then the ×; and the backdrop.
	const button = page.locator('.spine .hud .corner .zoom-drawing');
	await button.click();
	expect(await zoomOpen(page), `the Zoom drawing button opens it (${at})`);
	await page.locator('dialog.zoom .close').click();
	expect(!(await zoomOpen(page)), `the × closes it (${at})`);
	expect(
		(await focused(page)).includes('zoom-drawing'),
		`focus returns to the button after the × (${at})`
	);
	await button.click();
	await page.mouse.click(4, viewport.height - 4);
	expect(!(await zoomOpen(page)), `a click on the backdrop closes it (${at})`);
	await context.close();
}

// Z typed into the AI box types; it opens nothing.
{
	const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
	const page = await context.newPage();
	await open(page, 'western-civ/prometheus');
	const aiTab = page.locator('[role="tab"]#tab-ai');
	if (await aiTab.count()) await aiTab.click();
	const box = page.locator('.ai textarea').first();
	if (await box.count()) {
		await box.click();
		await page.keyboard.type('zz');
		expect(!(await zoomOpen(page)), `Z typed in the AI box opens nothing`);
		expect((await box.inputValue()).endsWith('zz'), `Z typed in the AI box types`);
	} else {
		console.log('note: no AI box on this edition; the typing check is skipped');
	}
	await context.close();
}

// A frame with no drawing: stripped from every body fetched, then End.
{
	const context = await browser.newContext({
		viewport: { width: 1280, height: 800 },
		reducedMotion: 'reduce'
	});
	const page = await context.newPage();
	await page.route('**/api/frame/**', async (route) => {
		const response = await route.fetch({
			headers: { ...route.request().headers(), 'if-none-match': '' }
		});
		const body = await response.json().catch(() => null);
		if (!body) return route.fulfill({ response });
		body.svg = null;
		await route.fulfill({ response, json: body });
	});
	await open(page, 'western-civ/prometheus');
	await page.locator('.spine [role="slider"]').focus();
	await page.keyboard.press('End');
	await page.waitForLoadState('networkidle');
	await page.waitForTimeout(300);
	const drawn = await page.locator('.spine .scene .illustration').count();
	expect(drawn === 0, `the stripped frame has no drawing in the scene (${drawn})`);
	const button = page.locator('.spine .hud .corner .zoom-drawing');
	expect(
		(await button.getAttribute('aria-disabled')) === 'true',
		`the Zoom drawing button is marked unavailable`
	);
	await page.keyboard.press('z');
	expect(!(await zoomOpen(page)), `Z on a frame with no drawing opens nothing`);
	await button.click({ force: true });
	expect(!(await zoomOpen(page)), `the unavailable button opens nothing`);
	await page.mouse.move(640, 700);
	await page.waitForTimeout(900);
	await button.hover();
	await untilTip(page);
	expect(
		/no drawing/.test(
			await tip(page)
				.innerText()
				.catch(() => '')
		),
		`its tooltip says there is no drawing`
	);
	await context.close();
}

// ---- Pop-ups in view (korg 3552) -------------------------------------------
// The contents and bookmarks panels hang from their HUD buttons, and every icon
// added after them moves the buttons left: on a smaller screen the contents ran
// off the window's left edge (sprint 050). Each stays in the window at every width
// from a narrow laptop to a wide desktop; under 40rem each is a sheet anyway.
for (const width of [700, 800, 900, 1024, 1280, 1440, 1920]) {
	const context = await browser.newContext({
		viewport: { width, height: 800 },
		reducedMotion: 'reduce'
	});
	const page = await context.newPage();
	await open(page, 'blood/hepatitis');
	for (const [name, button, panel] of [
		['contents', '.spine .hud .contents > button', '.spine .hud .contents .panel'],
		['bookmarks', '.spine .hud .bookmarks button[aria-expanded]', '.spine .hud .bookmarks .panel']
	]) {
		const control = page.locator(button).first();
		if (!(await control.count())) {
			expect(false, `${width}px: the ${name} button is in the HUD`);
			continue;
		}
		await control.click();
		await page.waitForTimeout(50);
		const box = await page.locator(panel).first().boundingBox();
		expect(
			box && box.x >= 0 && box.x + box.width <= width,
			`${width}px: the ${name} panel is in the window (${box ? `${Math.round(box.x)} to ${Math.round(box.x + box.width)}` : 'not shown'})`
		);
		await page.keyboard.press('Escape');
	}
	await context.close();
}

await browser.close();

for (const f of failures) console.log(`FAIL ${f}`);
console.log(`${checks - failures.length}/${checks} checks passed`);
process.exit(failures.length ? 1 : 0);
