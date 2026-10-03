// The Playwright and Chromium already on this machine, rather than a
// dependency of the repo: $PLAYWRIGHT_CORE (a path to playwright-core's
// index.mjs) or the bun or npx cache, and $CHROME or ~/.cache/ms-playwright's
// Chromium. Shared by the checks that drive a real browser (scene-fit,
// keys-check).
import { existsSync, readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

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

function playwright(fail) {
	const found = [
		process.env.PLAYWRIGHT_CORE,
		...newest(join(homedir(), '.bun/install/cache'), 'playwright-core@', 'index.mjs'),
		...newest(join(homedir(), '.npm/_npx'), '', 'node_modules/playwright-core/index.mjs')
	].filter(Boolean);
	if (!found.length) fail('no playwright-core found; set $PLAYWRIGHT_CORE to its index.mjs');
	return found[0];
}

function chrome(fail) {
	const cache = join(homedir(), '.cache/ms-playwright');
	const found = [
		process.env.CHROME,
		...newest(cache, 'chromium-', 'chrome-linux64/chrome'),
		...newest(cache, 'chromium_headless_shell-', 'chrome-linux64/chrome-headless-shell')
	].filter(Boolean);
	if (!found.length) fail('no Chromium found; set $CHROME');
	return found[0];
}

/** A launched headless Chromium; `fail` reports what could not be found and exits. */
export async function launch(fail) {
	const { chromium } = await import(pathToFileURL(playwright(fail)).href);
	return chromium.launch({ executablePath: chrome(fail) });
}
