import { readdir, readFile } from 'node:fs/promises';
import { basename, join } from 'node:path';
import { renderMarkdown } from './markdown';
import type { Frame, FrameFile, Manifest, Spine, Subject, Trail } from './model';
import { validate, type RawFrame, type RawSubject } from './validate';

/** A subject that failed validation; `problems` lists every one found. */
export class SubjectError extends Error {
	constructor(
		readonly dir: string,
		readonly problems: string[]
	) {
		super(`subject ${dir} is invalid:\n  ${problems.join('\n  ')}`);
		this.name = 'SubjectError';
	}
}

async function text(path: string): Promise<string | null> {
	try {
		return await readFile(path, 'utf8');
	} catch (e) {
		if ((e as NodeJS.ErrnoException).code === 'ENOENT') return null;
		throw e;
	}
}

/** Parsed JSON, undefined when the file is missing; a parse error names the file. */
async function json(path: string): Promise<unknown> {
	const source = await text(path);
	if (source === null) return undefined;
	try {
		return JSON.parse(source);
	} catch (e) {
		throw new Error(`${path}: ${(e as Error).message}`, { cause: e });
	}
}

async function entries(dir: string) {
	try {
		return await readdir(dir, { withFileTypes: true });
	} catch (e) {
		if ((e as NodeJS.ErrnoException).code === 'ENOENT') return [];
		throw e;
	}
}

/** Read a subject directory as-is: no checks, no rendering. */
export async function readSubject(dir: string): Promise<RawSubject> {
	const trails: RawSubject['trails'] = {};
	for (const e of await entries(join(dir, 'trails')))
		if (e.isFile() && e.name.endsWith('.json'))
			trails[e.name.slice(0, -'.json'.length)] = await json(join(dir, 'trails', e.name));

	const frames: RawSubject['frames'] = {};
	for (const e of await entries(join(dir, 'frames'))) {
		if (!e.isDirectory()) continue;
		const at = join(dir, 'frames', e.name);
		const svgs: RawFrame['svgs'] = {};
		for (const f of await entries(at))
			if (f.isFile() && f.name.endsWith('.svg')) svgs[f.name] = (await text(join(at, f.name)))!;
		frames[e.name] = {
			frame: await json(join(at, 'frame.json')),
			reading: await text(join(at, 'reading.md')),
			svgs
		};
	}

	return {
		manifest: await json(join(dir, 'subject.json')),
		spine: await json(join(dir, 'spine.json')),
		trails,
		frames
	};
}

/** Turn a raw subject into a renderable one; throws SubjectError if invalid. */
export function buildSubject(id: string, raw: RawSubject): Subject {
	const problems = validate(raw);
	if (problems.length) throw new SubjectError(id, problems);

	const manifest = raw.manifest as Manifest;
	const frames: Record<string, Frame> = {};
	for (const [dir, r] of Object.entries(raw.frames)) {
		const file = r.frame as FrameFile;
		frames[dir] = {
			...file,
			readingHtml: renderMarkdown(r.reading!),
			svg: file.scene.illustration ? r.svgs[file.scene.illustration] : null
		};
	}
	return {
		id,
		title: manifest.title,
		palettes: manifest.palettes,
		spine: raw.spine as Spine,
		trails: Object.values(raw.trails) as Trail[],
		frames
	};
}

/** Load and validate `subjects/<id>/`-shaped content from `dir`. */
export async function loadSubject(dir: string): Promise<Subject> {
	return buildSubject(basename(dir), await readSubject(dir));
}
