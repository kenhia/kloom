// The Home button in a real browser (korg 3517): going home is a history
// entry at `/<subject>`, so the screen and the address always agree.
//
// - Home, by keyboard, shows the start screen and puts `/<subject>` in the
//   address bar;
// - a reload there stays on the start screen;
// - Back returns to the frame, and Forward comes home again;
// - Begin from home returns to the frame, with its address, and Back from
//   there stays in the reading rather than finding the start screen again.
//
//   node create-tools/home-check/home_check.mjs [--url URL] [--frame subject/frame]
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
	console.error(`home_check: ${message}`);
	process.exit(2);
}

const browser = await launch(fail);
const failures = [];
let checks = 0;
function expect(ok, what) {
	checks++;
	if (!ok) failures.push(what);
}

const context = await browser.newContext({
	viewport: { width: 1280, height: 800 },
	reducedMotion: 'reduce'
});
const page = await context.newPage();
const path = () => new URL(page.url()).pathname;
const start = page.locator('.start');
/** The start screen shown or gone, given a moment to settle either way. */
async function home(shown) {
	await start.waitFor({ state: shown ? 'visible' : 'detached', timeout: 3000 }).catch(() => {});
	return start.isVisible();
}

await page.goto(`${url}/${frame}`, { waitUntil: 'networkidle' });
await page.waitForSelector('.spine .scene');
expect(!(await home(false)), `a deep link opens on the frame, not the start screen`);

// 1. Home, by keyboard.
await page.locator('.shell .home').focus();
await page.keyboard.press('Enter');
expect(await home(true), `Enter on Home shows the start screen`);
await page.waitForURL(`**/${subject}`, { timeout: 3000 }).catch(() => {});
expect(path() === `/${subject}`, `Home puts /${subject} in the address bar (${path()})`);

// 2. A reload stays home.
await page.reload({ waitUntil: 'networkidle' });
expect(await home(true), `a reload after Home stays on the start screen (${path()})`);

// 3. Back to the frame, Forward home again.
await page.goBack({ waitUntil: 'networkidle' });
expect(path() === `/${frame}`, `Back returns to /${frame} (${path()})`);
expect(!(await home(false)), `Back returns to the reading, not the start screen`);
await page.goForward({ waitUntil: 'networkidle' });
expect(path() === `/${subject}`, `Forward comes back to /${subject} (${path()})`);
expect(await home(true), `Forward shows the start screen again`);

// 4. Begin from home: the frame's address, and Back stays in the reading.
await page.goBack({ waitUntil: 'networkidle' });
/** A click that counts as a failed check, rather than a crash, when there is nothing to click. */
const press = (selector, what) =>
	page
		.locator(selector)
		.click({ timeout: 3000 })
		.then(() => true)
		.catch(() => (expect(false, what), false));
if (await press('.shell .home', `Home is there to press after Back (${path()})`)) await home(true);
await press('.start .begin', `Begin is there to press on the start screen (${path()})`);
expect(!(await home(false)), `Begin from home returns to the reading`);
await page.waitForURL((u) => u.pathname !== `/${subject}`, { timeout: 3000 }).catch(() => {});
expect(path().startsWith(`/${subject}/`), `Begin names a frame in the address (${path()})`);
await page.goBack({ waitUntil: 'networkidle' });
expect(!(await home(false)), `Back after Begin stays in the reading (${path()})`);

await context.close();
await browser.close();

for (const f of failures) console.log(`FAIL ${f}`);
console.log(`${checks - failures.length}/${checks} checks passed`);
process.exit(failures.length ? 1 : 0);
