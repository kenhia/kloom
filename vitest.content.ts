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
 */
export default async function () {
	const dir = mkdtempSync(join(tmpdir(), 'kloom-content-'));
	const out = join(dir, 'content.db');
	const report = await compileContent({
		subjectsDir: resolve('subjects'),
		namesDir: resolve('names'),
		out,
		compiler: engineDigest(resolve('engine')) ?? '',
		strict: true,
		added: await gitAddedDates(resolve('subjects'))
	});
	if (report.nameProblems.length) throw new Error(`names: ${report.nameProblems.join('; ')}`);
	process.env.KLOOM_CONTENT_DB = out;
	return () => rmSync(dir, { recursive: true, force: true });
}
