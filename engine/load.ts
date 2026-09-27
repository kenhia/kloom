import { readdir, readFile } from 'node:fs/promises';
import { basename, join } from 'node:path';
import { captionCredit, needsCaption } from './citation';
import { renderMarkdown } from './markdown';
import type { Frame, FrameFile, Manifest, Spine, Subject, Trail } from './model';
import { MEDIA_FILE, validate, type RawFrame, type RawSubject } from './validate';

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
		const media: string[] = [];
		for (const f of await entries(at)) {
			if (!f.isFile()) continue;
			if (f.name.endsWith('.svg')) svgs[f.name] = (await text(join(at, f.name)))!;
			if (MEDIA_FILE.test(f.name)) media.push(f.name);
		}
		frames[e.name] = {
			frame: await json(join(at, 'frame.json')),
			reading: await text(join(at, 'reading.md')),
			svgs,
			media: media.sort()
		};
	}

	return {
		manifest: await json(join(dir, 'subject.json')),
		spine: await json(join(dir, 'spine.json')),
		trails,
		frames
	};
}

export interface BuildOptions {
	/** URL prefix a frame's media is served under: `<base>/<frame>/<file>`. */
	mediaBase?: string;
}

/** Turn a raw subject into a renderable one; throws SubjectError if invalid. */
export function buildSubject(id: string, raw: RawSubject, options: BuildOptions = {}): Subject {
	const base = options.mediaBase ?? '/media';
	const problems = validate(raw);
	if (problems.length) throw new SubjectError(id, problems);

	const manifest = raw.manifest as Manifest;
	const frames: Record<string, Frame> = {};
	for (const [dir, r] of Object.entries(raw.frames)) {
		const file = r.frame as FrameFile;
		const media = new Map(
			(file.citations ?? []).filter((c) => c.kind === 'media').map((c) => [c.file, c])
		);
		const image = (href: string) => {
			const c = media.get(href);
			if (!c) return null;
			const src = `${base}/${encodeURIComponent(dir)}/${encodeURIComponent(href)}`;
			return needsCaption(c.licence!) ? { src, credit: captionCredit(c) } : { src };
		};
		frames[dir] = {
			...file,
			readingHtml: renderMarkdown(r.reading!, { image }),
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
export async function loadSubject(dir: string, options?: BuildOptions): Promise<Subject> {
	return buildSubject(basename(dir), await readSubject(dir), options);
}

const MEDIA_TYPES: Record<string, string> = {
	png: 'image/png',
	jpg: 'image/jpeg',
	jpeg: 'image/jpeg',
	webp: 'image/webp',
	gif: 'image/gif',
	svg: 'image/svg+xml'
};

/**
 * One media file from a frame's directory, or null. Both names are checked
 * against the same rules validation uses, so no path can leave the subject.
 */
export async function readMedia(
	dir: string,
	frame: string,
	file: string
): Promise<{ body: Buffer; type: string } | null> {
	if (!/^[\w-]+$/.test(frame) || !MEDIA_FILE.test(file)) return null;
	try {
		const body = await readFile(join(dir, 'frames', frame, file));
		return { body, type: MEDIA_TYPES[file.split('.').pop()!.toLowerCase()] };
	} catch (e) {
		if ((e as NodeJS.ErrnoException).code === 'ENOENT') return null;
		throw e;
	}
}

/**
 * A frame's reading as authored (markdown), or null. The model is given this
 * rather than the rendered HTML.
 */
export async function readReading(dir: string, frame: string): Promise<string | null> {
	if (!/^[\w-]+$/.test(frame)) return null;
	return text(join(dir, 'frames', frame, 'reading.md'));
}
