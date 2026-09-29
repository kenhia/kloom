import { readdir, readFile } from 'node:fs/promises';
import { basename, join } from 'node:path';
import { captionCredit, keySources, needsCaption } from './citation';
import type { GraphSubject } from './graph';
import { nameRefs, renderMarkdown } from './markdown';
import { buildNames, type Name } from './names';
import { sanitiseSvg } from './svg';
import type { Connection, Frame, FrameFile, Manifest, Spine, Subject, Trail } from './model';
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
		// A hidden directory is never a frame (grow stages a new one as `.grow-<id>`).
		if (!e.isDirectory() || e.name.startsWith('.')) continue;
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
	/** The name registry's ids: given, a mark on any other name is invalid. */
	names?: ReadonlySet<string>;
}

/** Turn a raw subject into a renderable one; throws SubjectError if invalid. */
export function buildSubject(id: string, raw: RawSubject, options: BuildOptions = {}): Subject {
	const base = options.mediaBase ?? '/media';
	const problems = validate(raw, { names: options.names });
	if (problems.length) throw new SubjectError(id, problems);

	const manifest = raw.manifest as Manifest;
	const frames: Record<string, Frame> = {};
	for (const [dir, r] of Object.entries(raw.frames)) {
		const file = r.frame as FrameFile;
		const media = new Map(file.citations.filter((c) => c.kind === 'media').map((c) => [c.file, c]));
		const image = (href: string) => {
			const c = media.get(href);
			if (!c) return null;
			const src = `${base}/${encodeURIComponent(dir)}/${encodeURIComponent(href)}`;
			const credit = needsCaption(c.licence!) ? { credit: captionCredit(c) } : {};
			// An SVG is inlined, re-serialised, so a chart takes the reader's palette.
			const svg = href.endsWith('.svg')
				? sanitiseSvg(r.svgs[href], {
						idPrefix: `${dir}-${href.slice(0, -'.svg'.length)}-`.replace(/[^\w-]/g, '-'),
						decorative: true
					}).svg
				: undefined;
			return { src, ...credit, ...(svg ? { svg } : {}) };
		};
		frames[dir] = {
			...file,
			sources: keySources(file.citations),
			readingHtml: renderMarkdown(r.reading!, { image }),
			// The re-serialised parse, never the file's own text (engine/svg.ts).
			svg: file.scene.illustration ? sanitiseSvg(r.svgs[file.scene.illustration]).svg : null
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

/**
 * The name registry: every `<id>.json` in `dir` (docs/design.md
 * §Connections). A missing directory is an empty registry. A file that is
 * invalid is left out and named in `problems`.
 */
export async function loadNames(
	dir: string
): Promise<{ names: Record<string, Name>; problems: string[] }> {
	const files: Record<string, unknown> = {};
	const problems: string[] = [];
	for (const e of await entries(dir)) {
		if (!e.isFile() || !e.name.endsWith('.json')) continue;
		try {
			files[e.name.slice(0, -'.json'.length)] = await json(join(dir, e.name));
		} catch (err) {
			problems.push((err as Error).message);
		}
	}
	const built = buildNames(files);
	return { names: built.names, problems: [...problems, ...built.problems] };
}

type Obj = Record<string, unknown>;
const isObj = (v: unknown): v is Obj => typeof v === 'object' && v !== null && !Array.isArray(v);

/**
 * What the graph index needs from a subject (engine/graph.ts), read lightly:
 * each frame's title, position, connections and marked names, in spine
 * order, main spine first. Nothing is rendered or validated, so another
 * subject's page costs little; a frame that cannot be read is left out.
 */
export async function readGraphSubject(dir: string, id = basename(dir)): Promise<GraphSubject> {
	const manifest = (await json(join(dir, 'subject.json')).catch(() => undefined)) as
		Obj | undefined;
	const spines: [string | null, unknown][] = [
		[null, await json(join(dir, 'spine.json')).catch(() => undefined)]
	];
	for (const e of await entries(join(dir, 'trails')))
		if (e.isFile() && e.name.endsWith('.json')) {
			const t = (await json(join(dir, 'trails', e.name)).catch(() => undefined)) as Obj;
			if (isObj(t)) spines.push([typeof t.title === 'string' ? t.title : null, t.spine]);
		}
	const frames: GraphSubject['frames'] = [];
	for (const [trail, spine] of spines) {
		const segments = isObj(spine) && Array.isArray(spine.segments) ? spine.segments : [];
		for (const seg of segments)
			for (const frame of isObj(seg) && Array.isArray(seg.frames) ? seg.frames : []) {
				if (typeof frame !== 'string' || !/^[\w-]+$/.test(frame)) continue;
				const at = join(dir, 'frames', frame);
				const file = (await json(join(at, 'frame.json')).catch(() => undefined)) as Obj;
				if (!isObj(file) || !isObj(file.scene) || !isObj(file.position)) continue;
				const reading = (await text(join(at, 'reading.md'))) ?? '';
				frames.push({
					subject: id,
					frame,
					title: `${file.scene.headline} ${file.scene.accent}`,
					label: String(file.position.label),
					trail,
					connections: Array.isArray(file.connections)
						? (file.connections as Connection[]).filter(
								(c) => isObj(c) && typeof c.to === 'string' && typeof c.why === 'string'
							)
						: [],
					names: [...new Set(nameRefs(reading))]
				});
			}
	}
	return {
		id,
		title: isObj(manifest) && typeof manifest.title === 'string' ? manifest.title : id,
		frames
	};
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
