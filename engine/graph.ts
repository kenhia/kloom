import type { Connection } from './model';
import type { Name, NameKind } from './names';

/**
 * The graph index (docs/design.md §Connections, korg 3439): every subject's
 * frames, the names their readings mark, and the connections between frames,
 * rebuilt at load from all the subjects served. Nothing in it is stored
 * twice: backlinks and a name's appearances are derived here.
 *
 * A connection or a home frame whose target is missing is detached, never a
 * failure: subjects may be kept apart and change on their own. The gate
 * checks the repository's own content with `graphProblems`.
 */

/** One frame as the graph knows it: enough to list it and to jump to it. */
export interface GraphFrame {
	subject: string;
	frame: string;
	/** Headline and accent. */
	title: string;
	/** What it is about, plainly (sprint 020). */
	topic: string;
	/** The position label. */
	label: string;
	/** The trail it is on, by title; null on the main spine. */
	trail: string | null;
}

/** What the graph reads from one subject, frames in spine order. */
export interface GraphSubject {
	id: string;
	title: string;
	frames: (GraphFrame & {
		connections: Connection[];
		/** The names its reading marks, each once, in order. */
		names: string[];
	})[];
}

export interface Link {
	/** `<subject>/<frame>`, as the key of `frames`. */
	from: string;
	to: string;
	why: string;
}

export interface Graph {
	/** Subject titles by id. */
	subjects: Record<string, string>;
	/** By `<subject>/<frame>`. */
	frames: Map<string, GraphFrame>;
	names: Record<string, Name>;
	/** The frames that mark each name, by name id. */
	mentions: Map<string, string[]>;
	links: Link[];
}

export const frameKey = (subject: string, frame: string) => `${subject}/${frame}`;

export function buildGraph(subjects: GraphSubject[], names: Record<string, Name>): Graph {
	const graph: Graph = {
		subjects: {},
		frames: new Map(),
		names,
		mentions: new Map(),
		links: []
	};
	for (const s of subjects) {
		graph.subjects[s.id] = s.title;
		for (const { connections, names: marked, ...f } of s.frames) {
			const key = frameKey(s.id, f.frame);
			graph.frames.set(key, f);
			for (const c of connections) graph.links.push({ from: key, to: c.to, why: c.why });
			for (const id of marked) graph.mentions.set(id, [...(graph.mentions.get(id) ?? []), key]);
		}
	}
	return graph;
}

/**
 * What is wrong with the repository's own links: a connection to a frame
 * that is not there, or to itself, or stored on both ends; a name whose home
 * is not a frame; a name marked but not registered. At load these are shown
 * detached; the gate refuses them.
 */
export function graphProblems(graph: Graph): string[] {
	const problems: string[] = [];
	const pairs = new Set<string>();
	for (const l of graph.links) {
		if (l.to === l.from) problems.push(`${l.from}: connects to itself`);
		else if (!graph.frames.has(l.to)) problems.push(`${l.from}: connects to ${l.to}, not a frame`);
		if (pairs.has(`${l.to} ${l.from}`))
			problems.push(`${l.from}: ${l.to} already connects to it; store a connection on one end`);
		pairs.add(`${l.from} ${l.to}`);
	}
	for (const [id, n] of Object.entries(graph.names))
		if (n.home && !graph.frames.has(n.home))
			problems.push(`names/${id}.json: home ${n.home} is not a frame`);
	for (const [id, at] of graph.mentions)
		if (!graph.names[id]) problems.push(`${at[0]}: marks "${id}", not in the name registry`);
	return problems;
}

/** A connection as one of its frames shows it: the other end, and why. */
export interface FrameLink {
	/** Stored on this frame (out), or on the other one (in). */
	direction: 'out' | 'in';
	why: string;
	subject: string;
	subjectTitle: string;
	frame: string;
	/** The other frame's title, topic and position; absent when it is detached. */
	title?: string;
	topic?: string;
	label?: string;
	trail?: string | null;
	/** Its target is not a frame (any more). */
	detached: boolean;
}

/** One line of a name card: a frame the name appears on. */
export type CardEntry = GraphFrame;

/** A name's card (§Connections): what it is, then where it appears. */
export interface NameCard {
	id: string;
	name: string;
	kind: NameKind;
	description: string;
	wikidata: string | null;
	/** The frame chiefly about it, listed first; null when there is none. */
	home: CardEntry | null;
	/** Where else it appears, by subject: the reader's subject first. */
	groups: { subject: string; subjectTitle: string; entries: CardEntry[] }[];
}

/**
 * What one frame's reading shows of the graph (docs/design.md §Serving):
 * its connections, both ways, and the cards of the names its reading marks.
 */
export interface FrameLinks {
	connections: FrameLink[];
	names: Record<string, NameCard>;
}

function linkTo(graph: Graph, key: string, direction: FrameLink['direction'], why: string) {
	const [subject, frame] = key.split('/');
	const f = graph.frames.get(key);
	return {
		direction,
		why,
		subject,
		subjectTitle: graph.subjects[subject] ?? subject,
		frame,
		...(f ? { title: f.title, topic: f.topic, label: f.label, trail: f.trail } : {}),
		detached: !f
	};
}

/** A name's card as a reader in `subject` sees it. Null for a name the registry lacks. */
export function nameCard(graph: Graph, id: string, subject: string): NameCard | null {
	const n = graph.names[id];
	if (!n) return null;
	const home = (n.home && graph.frames.get(n.home)) || null;
	const bySubject = new Map<string, CardEntry[]>();
	for (const key of graph.mentions.get(id) ?? []) {
		const f = graph.frames.get(key)!;
		if (f === home) continue;
		bySubject.set(f.subject, [...(bySubject.get(f.subject) ?? []), f]);
	}
	const title = (s: string) => graph.subjects[s] ?? s;
	const groups = [...bySubject]
		.map(([s, entries]) => ({ subject: s, subjectTitle: title(s), entries }))
		.sort(
			(a, b) =>
				Number(b.subject === subject) - Number(a.subject === subject) ||
				a.subjectTitle.localeCompare(b.subjectTitle)
		);
	return {
		id,
		name: n.name,
		kind: n.kind,
		description: n.description,
		wikidata: n.wikidata,
		home,
		groups
	};
}

/**
 * Every frame's links, by `<subject>/<frame>`: computed once per build of
 * the library, so a connection stored on another subject's frame shows here
 * as soon as either is built. A frame with none has empty links.
 */
export function linksByFrame(graph: Graph): Map<string, FrameLinks> {
	const out = new Map<string, FrameLinks>();
	for (const key of graph.frames.keys()) out.set(key, { connections: [], names: {} });
	const add = (key: string, link: FrameLink) => out.get(key)?.connections.push(link);
	for (const l of graph.links) {
		add(l.from, linkTo(graph, l.to, 'out', l.why));
		// A backlink only from a frame that is there.
		if (graph.frames.has(l.from)) add(l.to, linkTo(graph, l.from, 'in', l.why));
	}
	for (const [id, at] of graph.mentions)
		for (const key of at) {
			const links = out.get(key);
			const card = links && nameCard(graph, id, key.slice(0, key.indexOf('/')));
			if (card) links.names[id] = card;
		}
	return out;
}
