import { citationProblems } from './citation';
import { imageRefs } from './markdown';
import { LABEL_KINDS, type Spine } from './model';

/** One frame directory as read from disk, before anything is trusted. */
export interface RawFrame {
	/** Parsed `frame.json`, or undefined when the file is missing. */
	frame: unknown;
	/** `reading.md`, or null when missing. */
	reading: string | null;
	/** Every `.svg` in the directory, by file name. */
	svgs: Record<string, string>;
	/** Every media file the frame may serve (images, charts), by file name. */
	media: string[];
}

/** A subject directory as read from disk, before anything is trusted. */
export interface RawSubject {
	manifest: unknown;
	spine: unknown;
	/** Parsed `trails/<id>.json`, by file stem. */
	trails: Record<string, unknown>;
	/** By directory name under `frames/`. */
	frames: Record<string, RawFrame>;
}

type Obj = Record<string, unknown>;

const isObj = (v: unknown): v is Obj => typeof v === 'object' && v !== null && !Array.isArray(v);
const isText = (v: unknown): v is string => typeof v === 'string' && v.trim() !== '';
const COLOURS = ['background', 'ink', 'muted', 'accent', 'line'] as const;

/** Files a frame may serve to the reading pane: a plain name, an image type. */
export const MEDIA_FILE = /^[\w-][\w.-]*\.(png|jpe?g|webp|gif|svg)$/i;

/**
 * Markup a line drawing never needs: active or embedding elements, links of
 * any kind, event handlers (after whitespace, `/` or a quote), `javascript:`
 * and character references, which could spell any of these past a regex.
 */
const SVG_TRIPWIRE =
	/<\/?\s*(script|style|foreignObject|embed|iframe|object|a|use|image|animate|set)\b|[\s/"']on[a-z]+\s*=|href\s*=|javascript:|&#/i;

/**
 * What is wrong with an SVG that will be inlined as a drawing, or null.
 * A tripwire for honest mistakes, not a sanitiser: model-written SVG needs a
 * real allowlist before grow may write one (korg 3360).
 */
export function illustrationProblem(svg: string): string | null {
	if (!/^\s*<svg[\s>]/.test(svg)) return 'illustration must be an <svg> element';
	if (SVG_TRIPWIRE.test(svg))
		return 'illustration contains script, styles, links or event handlers';
	return null;
}

/**
 * Every problem with a subject, as `where: what` lines. Empty means valid.
 * Collects rather than throws, so one pass shows an author everything.
 */
export function validate(raw: RawSubject): string[] {
	const errors: string[] = [];
	const fail = (where: string, what: string) => errors.push(`${where}: ${what}`);

	const palettes = new Set<string>();
	if (!isObj(raw.manifest)) fail('subject.json', 'missing or not an object');
	else {
		if (!isText(raw.manifest.title)) fail('subject.json', 'title is required');
		const p = raw.manifest.palettes;
		if (!isObj(p) || Object.keys(p).length === 0)
			fail('subject.json', 'at least one palette is required');
		else
			for (const [name, palette] of Object.entries(p)) {
				palettes.add(name);
				if (!isObj(palette)) {
					fail(`subject.json palette ${name}`, 'not an object');
					continue;
				}
				if (palette.scheme !== 'dark' && palette.scheme !== 'light')
					fail(`subject.json palette ${name}`, 'scheme must be "dark" or "light"');
				for (const c of COLOURS)
					if (!isText(palette[c])) fail(`subject.json palette ${name}`, `${c} is required`);
			}
	}

	// Which spine lists each frame; a frame belongs to exactly one.
	const placed = new Map<string, string>();

	const checkSpine = (where: string, spine: unknown): spine is Spine => {
		if (!isObj(spine) || !Array.isArray(spine.segments) || spine.segments.length === 0) {
			fail(where, 'needs at least one segment');
			return false;
		}
		const ids = new Set<string>();
		spine.segments.forEach((seg: unknown, i) => {
			const at = `${where} segment ${i}`;
			if (!isObj(seg)) return fail(at, 'not an object');
			if (!isText(seg.id)) fail(at, 'id is required');
			else if (ids.has(seg.id)) fail(at, `duplicate segment id "${seg.id}"`);
			else ids.add(seg.id);
			if (!isText(seg.title)) fail(at, 'title is required');
			if (!LABEL_KINDS.includes(seg.labelKind as never))
				fail(at, `labelKind must be one of ${LABEL_KINDS.join(', ')}`);
			if (!Array.isArray(seg.frames) || seg.frames.length === 0)
				return fail(at, 'needs at least one frame');

			let previous: number | undefined;
			for (const id of seg.frames) {
				if (!isText(id) || !(id in raw.frames)) {
					fail(at, `unknown frame "${String(id)}"`);
					continue;
				}
				const other = placed.get(id);
				if (other) fail(at, `frame "${id}" is already on ${other}`);
				else placed.set(id, where);

				if (seg.labelKind !== 'date') continue;
				const frame = raw.frames[id].frame;
				const sort = isObj(frame) && isObj(frame.position) ? frame.position.sort : undefined;
				if (typeof sort !== 'number' || !Number.isFinite(sort)) {
					fail(at, `frame "${id}" needs a numeric position.sort in a date segment`);
					continue;
				}
				if (previous !== undefined && sort < previous)
					fail(at, `frame "${id}" (${sort}) is out of order after ${previous}`);
				previous = sort;
			}
		});
		return true;
	};

	const mainOk = checkSpine('spine.json', raw.spine);
	const mainFrames = new Set(
		mainOk
			? (raw.spine as Spine).segments.flatMap((s) => (Array.isArray(s.frames) ? s.frames : []))
			: []
	);

	for (const [stem, trail] of Object.entries(raw.trails)) {
		const where = `trails/${stem}.json`;
		if (!isObj(trail)) {
			fail(where, 'not an object');
			continue;
		}
		if (trail.id !== stem) fail(where, `id must match the file name ("${stem}")`);
		if (!isText(trail.title)) fail(where, 'title is required');
		if (!isText(trail.anchor) || !mainFrames.has(trail.anchor))
			fail(where, `unknown anchor "${String(trail.anchor)}" (must be a main-spine frame)`);
		checkSpine(where, trail.spine);
	}

	for (const [dir, { frame, reading, svgs, media }] of Object.entries(raw.frames)) {
		const where = `frames/${dir}`;
		if (!placed.has(dir)) fail(where, 'is not on any spine');
		if (!isObj(frame)) {
			fail(where, 'frame.json is missing or not an object');
			continue;
		}
		if (frame.id !== dir) fail(where, `id must match the directory name ("${dir}")`);
		if (!isObj(frame.position) || !isText(frame.position.label))
			fail(where, 'position.label is required');

		const scene = frame.scene;
		if (!isObj(scene)) fail(where, 'scene is required');
		else {
			if (!isText(scene.headline)) fail(where, 'scene.headline is required');
			if (!isText(scene.accent)) fail(where, 'scene.accent is required');
			if (!isText(scene.palette) || !palettes.has(scene.palette))
				fail(where, `unknown palette "${String(scene.palette)}"`);
			if (!Array.isArray(scene.metadata) || !scene.metadata.every((m) => typeof m === 'string'))
				fail(where, 'scene.metadata must be a list of strings');
			if (scene.counter !== undefined && !(isObj(scene.counter) && isText(scene.counter.value)))
				fail(where, 'scene.counter needs a value');
			if (scene.illustration !== undefined) {
				const svg = isText(scene.illustration) ? svgs[scene.illustration] : undefined;
				if (svg === undefined)
					fail(where, `illustration "${String(scene.illustration)}" is not in the directory`);
				else {
					// Inlined into the page, so it must be a drawing and nothing more.
					const problem = illustrationProblem(svg);
					if (problem) fail(where, problem);
				}
			}
		}

		if (!Array.isArray(frame.sources) || frame.sources.length === 0)
			fail(where, 'sources are required — every frame carries at least one');
		else
			frame.sources.forEach((s: unknown, i) => {
				if (!isObj(s) || !isText(s.title)) fail(where, `source ${i} needs a title`);
				else if (s.url !== undefined && !(isText(s.url) && /^https?:\/\//.test(s.url)))
					fail(where, `source ${i} url must be http(s)`);
			});

		// Citations are optional, but an image or chart the reading uses is not
		// shown without a media citation carrying its licence.
		const credited = new Set<string>();
		if (frame.citations !== undefined && !Array.isArray(frame.citations))
			fail(where, 'citations must be a list');
		else
			(frame.citations ?? []).forEach((c: unknown, i: number) => {
				for (const problem of citationProblems(c)) fail(`${where} citation ${i}`, problem);
				if (!isObj(c) || c.kind !== 'media' || !isText(c.file)) return;
				if (!media.includes(c.file))
					fail(`${where} citation ${i}`, `credits "${c.file}", which is not in the directory`);
				else if (isText(c.licence)) credited.add(c.file);
			});

		if (!isText(reading)) fail(where, 'reading.md is missing or empty');
		else
			for (const ref of imageRefs(reading)) {
				if (!MEDIA_FILE.test(ref) || !media.includes(ref))
					fail(where, `image "${ref}" must be an image file in the frame's directory`);
				else if (!credited.has(ref))
					fail(where, `image "${ref}" needs a media citation with a licence`);
			}
	}

	return errors;
}
