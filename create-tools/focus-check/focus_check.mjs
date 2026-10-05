// The character shortcuts after every way into the reading (korg 3561, 3562,
// 3563, 3564): they act anywhere in the shell but a text field or a dialog,
// so none of these leaves Z (or B) dead.
//
// - a deep link, Begin on the same subject, Begin on another, Enter on the
//   subject list, a resume (Continue) and Home then Esc: each lands focus
//   where docs/design.md §Start screen says (the spine, or Home after Esc),
//   and Z opens the drawing;
// - a click on the scene, or on a paragraph of the reading: Z still opens
//   the drawing, and B still bookmarks;
// - Enter after a click on the start screen's background begins;
// - and Z typed in the AI box stays in the box.
//
//   node create-tools/focus-check/focus_check.mjs [--url URL] [--frame subject/frame]
//
// Exits 1 on any failure.
import { launch } from '../lib/browser.mjs';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(name);
	return i < 0 ? fallback : args[i + 1];
};
const url = opt('--url', process.env.KLOOM_URL || 'http://localhost:5415');
const frame = opt('--frame', 'western-civ/prometheus');
const subject = frame.split('/')[0];

function fail(message) {
	console.error(`focus_check: ${message}`);
	process.exit(2);
}

const browser = await launch(fail);
const failures = [];
let checks = 0;
function expect(ok, what) {
	checks++;
	if (!ok) failures.push(what);
	if (process.env.FOCUS_CHECK_TRACE) console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`);
}

const context = await browser.newContext({
	viewport: { width: 1280, height: 800 },
	reducedMotion: 'reduce'
});
const page = await context.newPage();
const start = page.locator('.start');
const focused = () =>
	page.evaluate(() => {
		const a = document.activeElement;
		return a ? `${a.tagName.toLowerCase()}.${[...a.classList].join('.')}` : 'none';
	});
const inSpine = () => page.evaluate(() => !!document.activeElement?.closest('.spine'));
const onHome = () => page.evaluate(() => !!document.activeElement?.matches('.shell .home'));
const zoomOpen = () =>
	page.evaluate(() => !!document.querySelector('dialog.zoom')?.hasAttribute('open'));

/** The start screen shown or gone, given a moment to settle either way. */
async function home(shown) {
	await start.waitFor({ state: shown ? 'visible' : 'detached', timeout: 3000 }).catch(() => {});
	return start.isVisible();
}
/** The shell settled on a frame with its drawing. */
async function reading() {
	await home(false);
	await page.waitForSelector('.spine .scene', { timeout: 5000 }).catch(() => {});
	await page.waitForTimeout(150);
}
/** Z opens the drawing from where focus is, and Esc closes it again. */
async function zoomWorks(at) {
	await page.keyboard.press('z');
	await page
		.waitForFunction(() => document.querySelector('dialog.zoom')?.hasAttribute('open'), null, {
			timeout: 2000
		})
		.catch(() => {});
	const open = await zoomOpen();
	expect(open, `${at}: Z opens the drawing (focus: ${await focused()})`);
	// A tooltip showing on the focused control takes the first Esc.
	for (let i = 0; i < 3 && (await zoomOpen()); i++) await page.keyboard.press('Escape');
}
/** A click that counts as a failed check, rather than a crash, when there is nothing to click. */
const press = (locator, what) =>
	locator
		.click({ timeout: 3000 })
		.then(() => true)
		.catch(() => (expect(false, what), false));
/** The address moved off this subject, or a failed check when it did not. */
const leftSubject = (what) =>
	page
		.waitForURL((u) => !u.pathname.startsWith(`/${subject}`), { timeout: 5000 })
		.then(() => true)
		.catch(() => (expect(false, what), false));

/**
 * Home, by keyboard, and the start screen up. Not by a click: the pointer
 * would rest on the start screen's corner, whose tooltip takes the first Esc.
 */
async function goHome() {
	if (await start.isVisible()) return true;
	await page.mouse.move(640, 400);
	await page.locator('.shell .home').focus();
	await page.keyboard.press('Enter');
	const shown = await home(true);
	// Home is a navigation to /<subject>: a key before it lands is undone by it.
	await page.waitForURL(`**/${subject}`, { timeout: 3000 }).catch(() => {});
	// The start screen takes focus as it mounts; a key before then goes to the page.
	await page
		.waitForFunction(() => !!document.activeElement?.closest('.start'), null, { timeout: 2000 })
		.catch(() => {});
	return shown;
}
/** The subject list on the start screen moved to another subject than this one. */
async function selectOther() {
	const list = page.locator('.start [role="listbox"]');
	if (!(await list.count())) return false;
	await list.focus();
	await page.keyboard.press('Home');
	const chosen = (await list.getAttribute('aria-activedescendant')) ?? '';
	if (chosen.endsWith(`-${subject}`)) await page.keyboard.press('ArrowDown');
	return !((await list.getAttribute('aria-activedescendant')) ?? '').endsWith(`-${subject}`);
}

// 1. A deep link: the shell mounts begun.
await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
await reading();
expect(await inSpine(), `deep link: focus is on the spine (${await focused()})`);
await zoomWorks('deep link');

// 2. Begin on the same subject: reading starts, so the spine takes focus.
if (await goHome()) {
	await press(page.locator('.start .begin'), `Begin is there to press`);
	await reading();
	expect(await inSpine(), `Begin, same subject: focus is on the spine (${await focused()})`);
	await zoomWorks('Begin, same subject');
} else expect(false, `Home shows the start screen`);
await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
await reading();

// 3. Home, then Esc: focus goes back to Home, and Z still acts from there.
if (await goHome()) {
	await page.keyboard.press('Escape');
	await reading();
	expect(await onHome(), `Home, then Esc: focus returns to Home (${await focused()})`);
	await zoomWorks('Home, then Esc');
}

// 4. Begin on another subject: its shell mounts begun.
if ((await goHome()) && (await selectOther())) {
	await press(page.locator('.start .begin'), `Begin is there to press`);
	await leftSubject(`Begin on another subject opens it`);
	await reading();
	expect(await inSpine(), `Begin, another subject: focus is on the spine (${await focused()})`);
	// Its first frame may have no drawing, so C, which every frame has.
	await page.keyboard.press('c');
	const contents = page.locator('.shell .contents [aria-expanded="true"]');
	await contents.waitFor({ timeout: 2000 }).catch(() => {});
	expect(
		await contents.count(),
		`Begin, another subject: C opens the contents (${await focused()})`
	);
	await page.keyboard.press('Escape');
} else expect(false, `the start screen has a subject list to choose from`);

// 5. Enter on the list, another subject.
await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
await reading();
if ((await goHome()) && (await selectOther())) {
	await page.keyboard.press('Enter');
	await leftSubject(`Enter on the list opens another subject`);
	await reading();
	expect(await inSpine(), `Enter on the list: focus is on the spine (${await focused()})`);
}

// 6. A resume (Continue) in this subject, from a fresh load of its start screen.
await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
await reading();
await page.keyboard.press('ArrowRight');
await page.waitForTimeout(800);
await page.goto(`${url}/${subject}`, { waitUntil: 'networkidle' });
await home(true);
const resume = page.locator('.start .resume button').first();
if (await resume.count()) {
	await press(resume, `the resume is there to press`);
	await reading();
	expect(await inSpine(), `Continue: focus is on the spine (${await focused()})`);
	await page.keyboard.press('ArrowLeft');
	await page.waitForTimeout(300);
	await zoomWorks('Continue');
} else console.log('note: no reader on this server, so no resume to press; Continue is skipped');

// 7. Clicks on the scene and on the reading keep the shortcuts.
await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
await reading();
await press(page.locator('.spine .scene').first(), `the scene is there to click`);
await zoomWorks('a click on the scene');
await press(page.locator('.narrative p').first(), `a paragraph is there to click`);
await zoomWorks('a click on a paragraph');
const status = page.locator('.shell p.visually-hidden[role="status"]').first();
if (await page.locator('.shell .bookmarks').count()) {
	await press(page.locator('.narrative p').first(), `a paragraph is there to click`);
	await page.keyboard.press('b');
	await page.waitForTimeout(200);
	const said = (await status.textContent().catch(() => '')) ?? '';
	expect(/Bookmark/.test(said), `a click on a paragraph, then B, bookmarks (said: ${said})`);
	if (/^Bookmarked/.test(said)) await page.keyboard.press('b');
} else console.log('note: no bookmarks on this server; B after a click is skipped');

// 8. Enter after a click on the start screen's background begins.
if (await goHome()) {
	const box = await start.boundingBox();
	await page.mouse.click(box.x + 8, box.y + box.height - 8);
	await page.keyboard.press('Enter');
	expect(!(await home(false)), `Enter after a click on the start screen's background begins`);
	await reading();
}

// 9. Z typed in the AI box stays in the box.
{
	await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
	await reading();
	const aiTab = page.locator('[role="tab"]#tab-ai');
	if (await aiTab.count()) await aiTab.click();
	const box = page.locator('.ai textarea').first();
	if (await box.count()) {
		await box.click();
		await page.keyboard.type('zz');
		expect(!(await zoomOpen()), `Z typed in the AI box opens nothing`);
		expect((await box.inputValue()).endsWith('zz'), `Z typed in the AI box types`);
	} else console.log('note: no AI box on this edition; the typing check is skipped');
}

await context.close();
await browser.close();

for (const f of failures) console.log(`FAIL ${f}`);
console.log(`${checks - failures.length}/${checks} checks passed`);
process.exit(failures.length ? 1 : 0);
