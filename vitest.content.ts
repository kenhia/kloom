import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { compileContent, engineDigest, gitAddedDates } from './engine/content-db';

/**
 * The gate's library (docs/design.md §Serving): every subject compiled once,
 * strictly, before any test runs, so an invalid subject fails `just check`
 * here, with every problem named. The routes under test read it through
 * `$KLOOM_CONTENT_DB`, built by the compiler they would use themselves, so
 * they find it current.
 *
 * `KLOOM_TEST_SUBJECTS` and `KLOOM_TEST_NAMES` point it at an author's
 * checking copy, as they do the subject tests (sprint 049: since sprint 032
 * this setup compiled the live tree, so a copy's check failed on any other
 * author's half-written frame).
 */
export default async function () {
	const dir = mkdtempSync(join(tmpdir(), 'kloom-content-'));
	const out = join(dir, 'content.db');
	const subjectsDir = resolve(process.env.KLOOM_TEST_SUBJECTS || 'subjects');
	const report = await compileContent({
		subjectsDir,
		namesDir: resolve(process.env.KLOOM_TEST_NAMES || 'names'),
		out,
		compiler: engineDigest(resolve('engine')) ?? '',
		strict: true,
		added: await gitAddedDates(subjectsDir)
	});
	if (report.nameProblems.length) throw new Error(`names: ${report.nameProblems.join('; ')}`);
	process.env.KLOOM_CONTENT_DB = out;
	return () => rmSync(dir, { recursive: true, force: true });
}
