import { isDeepStrictEqual } from 'node:util';
import { nameRefs } from '../markdown';
import type { Spine, Trail } from '../model';
import { buildNames } from '../names';
import { sanitiseSvg } from '../svg';
import type { RawSubject } from '../validate';

/**
 * Grow (docs/design.md §Grow, korg 3364): a queued job that asks a model to
 * add frames or a trail to a copy of the subject, then checks that what came
 * back is additive, valid and safe before any of it is taken. This module is
 * the pure part: the job's shape, the prompt, and the growth check. Running
 * jobs, applying and committing are the host's (src/lib/server/grow.ts).
 */

/** What a job adds: main-spine frames, a trail from the anchor, or a frame with its trail. */
export const GROW_VERBS = ['frames', 'trail', 'both'] as const;
export type GrowVerb = (typeof GROW_VERBS)[number];

export type GrowStatus = 'queued' | 'running' | 'applying' | 'done' | 'failed';

/** A grow job as persisted, one JSON file per job, so the queue survives a restart. */
export interface GrowJob {
	kind: 'kloom.grow-job';
	version: 1;
	/** The time it was queued plus random hex, like an answer id; safe as a file name. */
	id: string;
	subject: string;
	verb: GrowVerb;
	/** The frame the reader was on (for a kept answer, the frame it was asked about). */
	anchor: string;
	/** The reader's words; may be empty when a kept answer says it all. */
	request: string;
	/** A kept answer to turn into content, by id. */
	kept: string | null;
	provider: string;
	/** Checked against the app config when queued, and fixed from then on. */
	model: string;
	web: boolean;
	/** Who asked for it (the host's reader identity); the commit is authored as them. */
	by?: { login: string; name: string; via: string };
	status: GrowStatus;
	/** Runs started; a job interrupted by a restart is retried once. */
	attempts: number;
	queuedAt: string;
	startedAt?: string;
	finishedAt?: string;
	/** What the model is doing now, for the AI pane. */
	progress?: string;
	/** On success. */
	result?: {
		frames: string[];
		trails: string[];
		/** Names it added to the registry. */
		names?: string[];
		commit: string | null;
		summary: string;
		/** Why the commit is not on the remote grow branch yet; the next push takes it. */
		pushError?: string;
		/**
		 * A dev grow's branch (`grow/dev-<host>`): the content went there for
		 * review, not into the subjects this server shows (korg 3442).
		 */
		branch?: string;
	};
	/** On failure: one line for the reader, and the validator's problems if any. */
	error?: string;
	problems?: string[];
}

export const GROW_VERB_TEXT: Record<GrowVerb, string> = {
	frames:
		'Add one to three frames to the MAIN spine, placed where they belong. Add no trail and change no trail.',
	trail:
		'Add a side trail of two to four frames branching from the anchor frame (extend the existing trail if one already branches from it). Do not change the main spine.',
	both: 'Add one new frame to the MAIN spine, and a side trail of two to four frames branching from that new frame.'
};

/** Where the anchor sits, for the prompt. */
export interface GrowAnchor {
	id: string;
	title: string;
	position: string;
	/** The main spine, or the trail's title. */
	on: string;
}

/** The job's own prompt; the instructions (skills/grow/SKILL.md) are the system prompt. */
export function growPrompt(
	job: Pick<GrowJob, 'verb' | 'request' | 'kept' | 'web'>,
	subjectTitle: string,
	anchor: GrowAnchor,
	today: string
): string {
	return [
		`Subject: ${subjectTitle}`,
		`Today: ${today}`,
		`Verb: ${job.verb}. ${GROW_VERB_TEXT[job.verb]}`,
		`Anchor frame: ${anchor.id} — "${anchor.title}" (${anchor.position}, on ${anchor.on}). Read frames/${anchor.id}/ first.`,
		job.kept
			? 'Kept answer: request/kept-answer.json holds an answer a reader kept. Turn it into this content.'
			: 'Kept answer: none.',
		job.web
			? 'Web: you may use WebSearch and WebFetch to find and check sources, and to pin Wikipedia revisions.'
			: 'Web: not available for this job. Cite only sources you know to be real.',
		'',
		'--- What the reader asked for ---',
		job.request.trim() || '(nothing beyond the verb and the kept answer)'
	].join('\n');
}

/** The prompt for a second turn over the same directory, when the first left problems. */
export function repairPrompt(problems: string[]): string {
	return [
		'kloom validated the directory and found these problems. Fix every one, by editing only the files you added (and spine.json or trails/ if needed). Change nothing else. Then reply with two or three sentences on what you added.',
		'',
		...problems.map((p) => `- ${p}`)
	].join('\n');
}

/** Frame ids along a spine, in order. */
const framesOf = (spine: Spine | undefined) =>
	Array.isArray(spine?.segments)
		? spine.segments.flatMap((s) => (Array.isArray(s?.frames) ? s.frames : []))
		: [];

/** Whether `sub` appears in `seq` in the same order (not necessarily adjacent). */
function inOrder(sub: string[], seq: string[]): boolean {
	let i = 0;
	for (const x of seq) if (x === sub[i]) i++;
	return i === sub.length;
}

/** Files a grown frame may hold: the frame, its reading, and drawings. */
const GROWN_FILE = /^(frame\.json|reading\.md|[a-z0-9][a-z0-9-]*\.svg)$/;
export const FRAME_ID = /^[a-z0-9][a-z0-9-]*$/;
/** Largest file a job may write, in characters. */
export const MAX_GROWN_FILE = 200_000;

/** What a job added, once `growthProblems` has passed it. */
export interface Growth {
	/** New frames on the main spine. */
	frames: string[];
	/** New frames on trails. */
	trailFrames: string[];
	/** Trail files that are new or changed. */
	trails: string[];
	/** Names added to the registry, by id; the host fills it in (`linkGrowthProblems`). */
	names?: string[];
}

/** The files in each new frame directory, as the host read them. */
export type GrownFiles = Record<string, Record<string, string>>;

/**
 * Every way `after` is not a clean addition to `before` under the job's verb,
 * as `where: what` lines; empty means it may be taken (the host still runs
 * `validate` over `after`). Existing content must be untouched and keep its
 * order; new frames need plain ids and may hold only a frame, a reading and
 * drawings, each drawing passing the sanitiser.
 */
export function growthProblems(
	before: RawSubject,
	after: RawSubject,
	files: GrownFiles,
	verb: GrowVerb,
	anchor: string
): { problems: string[]; growth: Growth } {
	const problems: string[] = [];
	const fail = (where: string, what: string) => problems.push(`${where}: ${what}`);

	if (!isDeepStrictEqual(before.manifest, after.manifest)) fail('subject.json', 'must not change');

	for (const [id, frame] of Object.entries(before.frames)) {
		const now = after.frames[id];
		if (!now) fail(`frames/${id}`, 'an existing frame was removed');
		else if (!isDeepStrictEqual(frame, now)) fail(`frames/${id}`, 'an existing frame was changed');
	}

	const mainBefore = framesOf(before.spine as Spine);
	const mainAfter = framesOf(after.spine as Spine);
	if (!inOrder(mainBefore, mainAfter))
		fail('spine.json', 'existing frames must all stay, in their order');
	for (const seg of (before.spine as Spine).segments) {
		const now = (after.spine as Spine | undefined)?.segments?.find((s) => s?.id === seg.id);
		if (!now) fail('spine.json', `segment "${seg.id}" was removed`);
		else if (now.title !== seg.title || now.labelKind !== seg.labelKind)
			fail('spine.json', `segment "${seg.id}" was renamed or changed kind`);
	}

	const trails: string[] = [];
	for (const [id, t] of Object.entries(before.trails)) {
		const was = t as Trail;
		const now = after.trails[id] as Trail | undefined;
		if (!now) {
			fail(`trails/${id}.json`, 'an existing trail was removed');
			continue;
		}
		if (now.title !== was.title || now.anchor !== was.anchor)
			fail(`trails/${id}.json`, 'an existing trail was renamed or re-anchored');
		if (!inOrder(framesOf(was.spine), framesOf(now.spine)))
			fail(`trails/${id}.json`, 'existing frames must all stay, in their order');
		if (!isDeepStrictEqual(was, now)) trails.push(id);
	}
	const newTrails = Object.keys(after.trails).filter((id) => !(id in before.trails));
	for (const id of newTrails)
		if (!FRAME_ID.test(id)) fail(`trails/${id}.json`, 'a trail id is lowercase words and dashes');
	trails.push(...newTrails);

	const added = Object.keys(after.frames).filter((id) => !(id in before.frames));
	for (const id of added) {
		if (!FRAME_ID.test(id)) fail(`frames/${id}`, 'a frame id is lowercase words and dashes');
		for (const [name, text] of Object.entries(files[id] ?? {})) {
			if (!GROWN_FILE.test(name))
				fail(
					`frames/${id}`,
					`"${name}" is not a file grow may write (frame.json, reading.md, *.svg)`
				);
			else if (text.length > MAX_GROWN_FILE) fail(`frames/${id}/${name}`, 'is too large');
			else if (name.endsWith('.svg'))
				for (const p of sanitiseSvg(text).problems) fail(`frames/${id}/${name}`, p);
		}
	}

	const addedSet = new Set(added);
	const frames = mainAfter.filter((id) => addedSet.has(id));
	const trailFrames = added.filter((id) => !frames.includes(id));
	const anchors = (ids: string[]) =>
		ids.map((id) => (after.trails[id] as Trail | undefined)?.anchor);

	if (added.length === 0) problems.push('the job added no frames');
	else if (verb === 'frames') {
		if (frames.length === 0) problems.push('verb frames: no new frame is on the main spine');
		if (trails.length) problems.push('verb frames: trails must not change');
	} else if (verb === 'trail') {
		if (frames.length) problems.push('verb trail: the main spine must not change');
		if (!mainAfter.includes(anchor))
			problems.push(`verb trail: "${anchor}" is not on the main spine`);
		if (anchors(trails).some((a) => a !== anchor))
			problems.push(`verb trail: every trail it adds or extends must branch from "${anchor}"`);
	} else {
		if (frames.length !== 1) problems.push('verb both: add exactly one new main-spine frame');
		if (
			trailFrames.length === 0 ||
			!anchors(trails).some((a) => a !== undefined && frames.includes(a))
		)
			problems.push('verb both: add a trail branching from the new frame');
	}

	return { problems, growth: { frames, trailFrames, trails } };
}

/**
 * Every way the names and connections a job wrote break §Connections' rules
 * for grow, as `where: what` lines; and the names it added. The registry
 * (`before` and `after` are its files by stem) may only grow: an existing
 * name stays as it was, and a new one must be a valid name for a thing the
 * registry does not already hold, marked in a frame the job wrote. A
 * connection or a new name's home must name a frame that is there: one of
 * `targets` (every served frame, as `<subject>/<frame>`) or one the job added.
 */
export function linkGrowthProblems(
	subject: string,
	before: Record<string, unknown>,
	after: Record<string, unknown>,
	grown: RawSubject,
	added: string[],
	targets: ReadonlySet<string>
): { problems: string[]; names: string[] } {
	const problems: string[] = [];
	const fail = (where: string, what: string) => problems.push(`${where}: ${what}`);
	const exists = (ref: string) =>
		targets.has(ref) || added.some((id) => ref === `${subject}/${id}`);

	for (const [stem, name] of Object.entries(before)) {
		if (!(stem in after)) fail(`names/${stem}.json`, 'an existing name was removed');
		else if (!isDeepStrictEqual(name, after[stem]))
			fail(`names/${stem}.json`, 'an existing name was changed; grow may only add names');
	}
	const names = Object.keys(after).filter((stem) => !(stem in before));
	// The registry's own rules, the existing names first so a clash is the new one's.
	const ordered = { ...before, ...Object.fromEntries(names.map((s) => [s, after[s]])) };
	for (const p of buildNames(ordered).problems)
		if (names.some((stem) => p.startsWith(`names/${stem}.json:`))) problems.push(p);

	const marked = new Set(added.flatMap((id) => nameRefs(grown.frames[id]?.reading ?? '')));
	for (const stem of names) {
		if (!marked.has(stem))
			fail(`names/${stem}.json`, 'a name grow adds must be marked in a frame it wrote');
		const home = (after[stem] as { home?: unknown } | null)?.home;
		if (typeof home === 'string' && !exists(home))
			fail(`names/${stem}.json`, `home ${home} is not a frame (see reference/frames.md)`);
	}

	for (const id of added) {
		const frame = grown.frames[id]?.frame as { connections?: unknown } | undefined;
		if (!Array.isArray(frame?.connections)) continue;
		for (const c of frame.connections as { to?: unknown }[]) {
			if (typeof c?.to !== 'string') continue;
			if (c.to === `${subject}/${id}`) fail(`frames/${id}`, 'connects to itself');
			else if (!exists(c.to))
				fail(`frames/${id}`, `connects to ${c.to}, not a frame (see reference/frames.md)`);
		}
	}
	return { problems, names };
}
