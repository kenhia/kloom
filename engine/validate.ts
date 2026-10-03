import { citationProblems, citedInProblems } from './citation';
import { imageRefs, kloomRefs, nameRefs } from './markdown';
import { EDIT_KINDS, LABEL_KINDS, type Spine } from './model';
import { FRAME_REF, NAME_HREF } from './names';
import { sanitiseSvg } from './svg';

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

/**
 * The longest a frame's topic may be: a map label, a list line. Set from the
 * backfill (sprint 020), whose longest topic fits with room to spare.
 */
export const TOPIC_MAX = 40;

/** A subject's subtitle is one line under its title, never a paragraph. */
export const SUBTITLE_MAX = 60;

/** The longest an edit's summary may be: a sentence or two, not a changelog of its own. */
export const EDIT_SUMMARY_MAX = 400;

/** A calendar date, `YYYY-MM-DD`, that is a real day. */
export function isDay(v: unknown): v is string {
	if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(v)) return false;
	const d = new Date(`${v}T00:00:00Z`);
	return !Number.isNaN(d.getTime()) && d.toISOString().slice(0, 10) === v;
}

/** Files a frame may serve to the reading pane: a plain name, an image type. */
export const MEDIA_FILE = /^[\w-][\w.-]*\.(png|jpe?g|webp|gif|svg)$/i;

export interface ValidateOptions {
	/**
	 * The name registry's ids (docs/design.md §Connections). Given, a reading
	 * that marks a name the registry lacks is invalid; the gate and grow give
	 * it. Absent, marks are checked for their form only, so serving a subject
	 * never depends on a registry that is kept apart from it.
	 */
	names?: ReadonlySet<string>;
	/** Collects what is worth an author's attention but is not wrong. */
	warnings?: string[];
}

/**
 * Every problem with a subject, as `where: what` lines. Empty means valid.
 * Collects rather than throws, so one pass shows an author everything.
 */
export function validate(raw: RawSubject, options: ValidateOptions = {}): string[] {
	const errors: string[] = [];
	const fail = (where: string, what: string) => errors.push(`${where}: ${what}`);
	const warn = (where: string, what: string) => options.warnings?.push(`${where}: ${what}`);

	const palettes = new Set<string>();
	if (!isObj(raw.manifest)) fail('subject.json', 'missing or not an object');
	else {
		if (!isText(raw.manifest.title)) fail('subject.json', 'title is required');
		const subtitle = raw.manifest.subtitle;
		if (subtitle !== undefined) {
			if (!isText(subtitle)) fail('subject.json', 'subtitle, when given, is a line of text');
			else if (subtitle.length > SUBTITLE_MAX)
				fail('subject.json', `subtitle is ${subtitle.length} characters; at most ${SUBTITLE_MAX}`);
		}
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
		// Checked once every palette is known: a counterpart may come later in the file.
		if (isObj(p))
			for (const [name, palette] of Object.entries(p)) {
				if (!isObj(palette) || palette.counterpart === undefined) continue;
				const other = p[palette.counterpart as string];
				if (!isText(palette.counterpart) || !isObj(other))
					fail(
						`subject.json palette ${name}`,
						`unknown counterpart "${String(palette.counterpart)}"`
					);
				else if (other.scheme === palette.scheme)
					fail(
						`subject.json palette ${name}`,
						`counterpart "${palette.counterpart}" must be of the other scheme`
					);
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
			if (seg.palette !== undefined && (!isText(seg.palette) || !palettes.has(seg.palette)))
				fail(at, `unknown palette "${String(seg.palette)}"`);
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
		if (trail.added !== undefined && !isDay(trail.added))
			fail(where, 'added, when given, is a date: YYYY-MM-DD');
		if (!isText(trail.anchor) || !mainFrames.has(trail.anchor))
			fail(where, `unknown anchor "${String(trail.anchor)}" (must be a main-spine frame)`);
		checkSpine(where, trail.spine);
	}

	// The accent word is a frame's signature: no two in a subject share one.
	const accents = new Map<string, string>();
	// A topic names a frame plainly, so no two in a subject share one either.
	const topics = new Map<string, string>();

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

		// The topic (sprint 020): what the frame is about, in a plain title, where
		// the headline is evocative and the position label may be a date.
		if (!isText(frame.topic)) fail(where, 'topic is required');
		else {
			const topic = frame.topic.trim();
			const accent =
				isObj(frame.scene) && isText(frame.scene.accent)
					? frame.scene.accent.trim().replace(/[.!?]+$/, '')
					: '';
			if (topic.length > TOPIC_MAX)
				fail(where, `topic is ${topic.length} characters; at most ${TOPIC_MAX}`);
			else if (/[.!]$/.test(topic)) fail(where, 'topic is a title: no closing "." or "!"');
			else if (
				accent.length > 1 &&
				new RegExp(`(^|\\W)${accent.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(\\W|$)`).test(topic)
			)
				fail(where, `topic must say what the frame is about, not repeat its accent "${accent}"`);
			const other = topics.get(topic.toLowerCase());
			if (other) fail(where, `topic "${topic}" is already frames/${other}'s`);
			else topics.set(topic.toLowerCase(), dir);
		}

		const scene = frame.scene;
		if (!isObj(scene)) fail(where, 'scene is required');
		else {
			if (!isText(scene.headline)) fail(where, 'scene.headline is required');
			if (!isText(scene.accent)) fail(where, 'scene.accent is required');
			else {
				const word = scene.accent
					.trim()
					.toUpperCase()
					.replace(/[.!?]+$/, '');
				const other = accents.get(word);
				if (other) fail(where, `accent "${word}" is already frames/${other}'s`);
				else accents.set(word, dir);
			}
			if (!isText(scene.palette) || !palettes.has(scene.palette))
				fail(where, `unknown palette "${String(scene.palette)}"`);
			if (!Array.isArray(scene.metadata) || !scene.metadata.every((m) => typeof m === 'string'))
				fail(where, 'scene.metadata must be a list of strings');
			if (scene.counter !== undefined && !(isObj(scene.counter) && isText(scene.counter.value)))
				fail(where, 'scene.counter needs a value');
			if (
				scene.dedication !== undefined &&
				!(
					isObj(scene.dedication) &&
					isText(scene.dedication.kicker) &&
					isText(scene.dedication.name) &&
					(scene.dedication.note === undefined || isText(scene.dedication.note))
				)
			)
				fail(where, 'scene.dedication needs a kicker and a name, and a note only as text');
			if (scene.illustration !== undefined) {
				const svg = isText(scene.illustration) ? svgs[scene.illustration] : undefined;
				if (svg === undefined)
					fail(where, `illustration "${String(scene.illustration)}" is not in the directory`);
				else {
					// Inlined into the page, so it must be a drawing and nothing more.
					for (const problem of sanitiseSvg(svg).problems) fail(where, `illustration: ${problem}`);
				}
			}
		}

		if (
			frame.asOf !== undefined &&
			!(isText(frame.asOf) && /^\d{4}-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?$/.test(frame.asOf))
		)
			fail(where, 'asOf must be YYYY-MM or YYYY-MM-DD');

		// When it was added (korg 3525): git says, and this overrides it.
		if (frame.added !== undefined && !isDay(frame.added))
			fail(where, 'added, when given, is a date: YYYY-MM-DD');

		// Edits and corrections (korg 3526): each dated, of a kind, and saying
		// what changed; newest first, as the reading pane lists them.
		if (frame.edits !== undefined) {
			if (!Array.isArray(frame.edits)) fail(where, 'edits must be a list');
			else {
				let later: string | undefined;
				frame.edits.forEach((e: unknown, i: number) => {
					const at = `${where} edit ${i}`;
					if (!isObj(e)) return fail(at, 'not an object');
					if (!isDay(e.date)) fail(at, 'date must be YYYY-MM-DD');
					else {
						if (later !== undefined && e.date > later)
							fail(at, `${e.date} comes after ${later}: edits are listed newest first`);
						later = e.date;
					}
					if (!EDIT_KINDS.includes(e.kind as never))
						fail(at, `kind must be one of ${EDIT_KINDS.join(', ')}`);
					if (!isText(e.summary)) fail(at, 'summary is required: what changed, and why');
					else if (e.summary.trim().length > EDIT_SUMMARY_MAX)
						fail(
							at,
							`summary is ${e.summary.trim().length} characters; at most ${EDIT_SUMMARY_MAX}`
						);
					for (const k of Object.keys(e))
						if (!['date', 'kind', 'summary'].includes(k)) fail(at, `unknown field "${k}"`);
				});
			}
		}

		// Connections (§Connections): to a frame anywhere, each saying why. A
		// missing target is not checked here: it is shown detached, and the
		// gate checks the repository's own across subjects (engine/graph.ts).
		if (frame.connections !== undefined) {
			if (!Array.isArray(frame.connections)) fail(where, 'connections must be a list');
			else {
				const to = new Set<string>();
				frame.connections.forEach((c: unknown, i: number) => {
					const at = `${where} connection ${i}`;
					if (!isObj(c)) return fail(at, 'not an object');
					if (!isText(c.to) || !FRAME_REF.test(c.to)) fail(at, 'to must be "<subject>/<frame>"');
					else if (to.has(c.to)) fail(at, `${c.to} is already a connection of this frame`);
					else to.add(c.to);
					if (!isText(c.why)) fail(at, 'why is required: a sentence on what connects them');
				});
			}
		}

		// Sources are derived from the key citations (sprint 008): a hand-kept
		// list beside them is the old form, and would silently go unshown.
		if (frame.sources !== undefined)
			fail(where, 'sources is not written any more: flag the key citations with "key": true');

		// Every frame flags at least one key source. An image or chart the
		// reading uses is not shown without a media citation carrying its licence.
		const credited = new Set<string>();
		if (!Array.isArray(frame.citations)) fail(where, 'citations are required, as a list');
		else if (!frame.citations.some((c) => isObj(c) && c.key === true))
			fail(where, 'every frame flags at least one key-source citation ("key": true)');
		if (Array.isArray(frame.citations))
			frame.citations.forEach((c: unknown, i: number) => {
				for (const problem of citationProblems(c)) fail(`${where} citation ${i}`, problem);
				if (!isObj(c) || c.kind !== 'media' || !isText(c.file)) return;
				if (!media.includes(c.file))
					fail(`${where} citation ${i}`, `credits "${c.file}", which is not in the directory`);
				else if (isText(c.licence)) credited.add(c.file);
			});
		// A source seen only in another work stands on that work's citation (sprint 029).
		if (Array.isArray(frame.citations))
			for (const { index, problem } of citedInProblems(frame.citations))
				fail(`${where} citation ${index}`, problem);

		if (!isText(reading)) fail(where, 'reading.md is missing or empty');
		else {
			// Name marks (§Connections): the only kloom: link, on a known name,
			// and once per frame, on its first mention.
			for (const href of kloomRefs(reading))
				if (!NAME_HREF.test(href)) fail(where, `"${href}" is not a name mark (kloom:e/<name id>)`);
			const named = new Set<string>();
			for (const id of nameRefs(reading)) {
				if (named.has(id)) warn(where, `"${id}" is marked again; only its first mention needs it`);
				else if (options.names && !options.names.has(id))
					fail(where, `"${id}" is not in the name registry`);
				named.add(id);
			}
		}
		if (isText(reading))
			for (const ref of imageRefs(reading)) {
				if (!MEDIA_FILE.test(ref) || !media.includes(ref))
					fail(where, `image "${ref}" must be an image file in the frame's directory`);
				else {
					if (!credited.has(ref))
						fail(where, `image "${ref}" needs a media citation with a licence`);
					// An SVG image is inlined (a chart takes the page's palette), so it
					// passes the same allowlist as an illustration.
					if (ref.endsWith('.svg'))
						for (const problem of sanitiseSvg(svgs[ref] ?? '').problems)
							fail(where, `image "${ref}": ${problem}`);
				}
			}
	}

	return errors;
}
