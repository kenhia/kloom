/**
 * The name registry (docs/design.md §Connections, korg 3439): the people,
 * places, organisations, artifacts, ideas and events the subjects mention,
 * one file each, shared by every subject. A reading marks a name's first
 * mention (`[Alan Turing](kloom:e/alan-turing)`), and the mark opens a card
 * saying where else the name appears.
 *
 * A name's `id` is local: the file's stem, and what a reading's mark names.
 * Its `wikidata` ID is the key that holds across repositories, so subjects
 * kept apart (korg 3387) agree on who "Turing" is without sharing a file.
 * A name with no Wikidata entry says so with `null`.
 */

export const NAME_KINDS = ['person', 'place', 'org', 'artifact', 'idea', 'event'] as const;
export type NameKind = (typeof NAME_KINDS)[number];

export interface Name {
	id: string;
	/** A Wikidata item (`Q7251`), or null when there is none. */
	wikidata: string | null;
	name: string;
	/** Other ways a reading writes it, for authors and search. */
	aliases?: string[];
	kind: NameKind;
	/** One line, shown at the top of the card. */
	description: string;
	/** The frame that is chiefly about it, as `<subject>/<frame>`; listed first. */
	home?: string;
}

/** What a name id looks like: the file's stem, and what a mark names. */
export const NAME_ID = /^[a-z0-9][a-z0-9-]*$/;

/** A frame anywhere: `<subject>/<frame>`. */
export const FRAME_REF = /^([a-z0-9][a-z0-9-]*)\/([\w-]+)$/;

/** A reading's mark on a name: `kloom:e/<id>`. */
export const NAME_HREF = /^kloom:e\/([a-z0-9][a-z0-9-]*)$/;

type Obj = Record<string, unknown>;
const isObj = (v: unknown): v is Obj => typeof v === 'object' && v !== null && !Array.isArray(v);
const isText = (v: unknown): v is string => typeof v === 'string' && v.trim() !== '';

/** Every problem with one name file, read from `<stem>.json`. Empty means valid. */
export function nameProblems(stem: string, raw: unknown): string[] {
	const problems: string[] = [];
	if (!NAME_ID.test(stem)) problems.push(`"${stem}" is not a name id (lower case, digits, -)`);
	if (!isObj(raw)) return [...problems, 'not an object'];
	if (raw.id !== stem) problems.push(`id must match the file name ("${stem}")`);
	if (!(raw.wikidata === null || (typeof raw.wikidata === 'string' && /^Q\d+$/.test(raw.wikidata))))
		problems.push('wikidata must be a Wikidata item id (Q…) or null');
	if (!isText(raw.name)) problems.push('name is required');
	if (!NAME_KINDS.includes(raw.kind as never))
		problems.push(`kind must be one of ${NAME_KINDS.join(', ')}`);
	if (!isText(raw.description)) problems.push('description is required');
	if (raw.aliases !== undefined && !(Array.isArray(raw.aliases) && raw.aliases.every(isText)))
		problems.push('aliases must be a list of strings');
	if (raw.home !== undefined && !(isText(raw.home) && FRAME_REF.test(raw.home)))
		problems.push('home must be "<subject>/<frame>"');
	return problems;
}

/**
 * The registry from its files, by stem: the names that are valid, and a
 * line for every problem. Two names sharing a Wikidata item are one thing
 * written twice, which is a problem too.
 */
export function buildNames(files: Record<string, unknown>): {
	names: Record<string, Name>;
	problems: string[];
} {
	const names: Record<string, Name> = {};
	const problems: string[] = [];
	const byItem = new Map<string, string>();
	for (const [stem, raw] of Object.entries(files)) {
		const found = nameProblems(stem, raw);
		if (found.length) {
			problems.push(...found.map((p) => `names/${stem}.json: ${p}`));
			continue;
		}
		const name = raw as Name;
		const other = name.wikidata && byItem.get(name.wikidata);
		if (other) problems.push(`names/${stem}.json: ${name.wikidata} is already names/${other}`);
		else if (name.wikidata) byItem.set(name.wikidata, stem);
		names[stem] = name;
	}
	return { names, problems };
}
