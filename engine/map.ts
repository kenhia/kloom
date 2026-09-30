import {
	forceCollide,
	forceLink,
	forceManyBody,
	forceRadial,
	forceSimulation,
	type SimulationLinkDatum,
	type SimulationNodeDatum
} from 'd3-force';
import type { Graph, Link } from './graph';
import type { NameKind } from './names';

/**
 * The map (docs/design.md §The map, korg 3441): the graph index drawn as a
 * picture you can move through. This file decides what each view holds, where
 * its nodes go, which labels fit and where an arrow key moves; the overlay
 * (engine/ui/MapOverlay.svelte) only draws the answer.
 *
 * Everything here is deterministic. The same view lays out the same way every
 * time: the layout runs to rest before anything is drawn, seeded by the view,
 * so there is no motion to reduce and nothing a reader sees twice moves.
 */

// ---------------------------------------------------------------------------
// The data: the graph as the browser gets it, once, when the map first opens.

export interface MapFrame {
	/** `<subject>/<frame>`. */
	key: string;
	/** Headline and accent: said in the details, after the topic. */
	title: string;
	/** What it is about: its name on the map (sprint 020). */
	topic: string;
	label: string;
	trail: string | null;
}

export interface MapName {
	name: string;
	kind: NameKind;
	description: string;
	/** Its home frame, when that is a frame. */
	home: string | null;
}

export interface MapData {
	/** In the order the app serves them: a subject's colour and shape follow it. */
	subjects: { id: string; title: string }[];
	frames: MapFrame[];
	/** Connections whose ends are both frames. */
	links: Link[];
	/** Names marked in at least one frame. */
	names: Record<string, MapName>;
	/** The frames that mark each name, in spine order. */
	mentions: Record<string, string[]>;
}

/** The graph, cut to what the map draws: detached links and unmarked names left out. */
export function mapDataOf(graph: Graph): MapData {
	const names: Record<string, MapName> = {};
	const mentions: Record<string, string[]> = {};
	for (const [id, at] of graph.mentions) {
		const n = graph.names[id];
		if (!n) continue;
		names[id] = {
			name: n.name,
			kind: n.kind,
			description: n.description,
			home: n.home && graph.frames.has(n.home) ? n.home : null
		};
		mentions[id] = at;
	}
	return {
		subjects: Object.entries(graph.subjects).map(([id, title]) => ({ id, title })),
		frames: [...graph.frames].map(([key, f]) => ({
			key,
			title: f.title,
			topic: f.topic,
			label: f.label,
			trail: f.trail
		})),
		links: graph.links.filter(
			(l) => l.from !== l.to && graph.frames.has(l.from) && graph.frames.has(l.to)
		),
		names,
		mentions
	};
}

export const subjectOf = (key: string) => key.slice(0, key.indexOf('/'));

/** The data indexed for the views: built once per load of the data. */
export class MapIndex {
	readonly frames = new Map<string, MapFrame>();
	readonly subjectTitles = new Map<string, string>();
	/** A frame's connections, both directions, each with its why. */
	readonly connected = new Map<string, { key: string; why: string }[]>();
	/** The names a frame marks. */
	readonly marks = new Map<string, string[]>();

	constructor(readonly data: MapData) {
		for (const s of data.subjects) this.subjectTitles.set(s.id, s.title);
		for (const f of data.frames) this.frames.set(f.key, f);
		const add = (a: string, b: string, why: string) =>
			this.connected.set(a, [...(this.connected.get(a) ?? []), { key: b, why }]);
		for (const l of data.links) {
			add(l.from, l.to, l.why);
			add(l.to, l.from, l.why);
		}
		for (const [id, at] of Object.entries(data.mentions))
			for (const key of at) this.marks.set(key, [...(this.marks.get(key) ?? []), id]);
	}

	subjectTitle = (id: string) => this.subjectTitles.get(id) ?? id;
	/** How many frames mark a name. */
	reach = (name: string) => this.data.mentions[name]?.length ?? 0;
}

// ---------------------------------------------------------------------------
// Views: what is on the map, and the same thing as lists.

export type MapTarget =
	| { view: 'frame'; key: string; steps: 1 | 2 }
	| { view: 'library' }
	| { view: 'subject'; id: string }
	| { view: 'name'; id: string };

export type MapNodeKind = 'frame' | 'name' | 'subject';

export interface MapNode {
	/** `f:<subject>/<frame>`, `n:<name>` or `s:<subject>`. */
	id: string;
	kind: MapNodeKind;
	/** On the map: the whole of it, in one line or two (`labelLines`). */
	lines: string[];
	/** Whole, for lists, the details and screen readers. */
	full: string;
	/** Said after the label: a position, a subject, a count. */
	detail: string;
	/** Whose colour and shape it wears; null for a name. */
	subject: string | null;
	/** Steps from the centre: 0, 1 or 2. */
	ring: number;
	/** Its radius on the map, in layout units. */
	size: number;
}

export type MapEdgeKind = 'connection' | 'mention' | 'between';

export interface MapEdge {
	a: string;
	b: string;
	kind: MapEdgeKind;
	/** A connection's why. */
	why?: string;
	/** Between subjects: how many connections join them. */
	weight: number;
}

/** One line of a list: a node, and what to say about it. */
export interface MapListItem {
	node: string;
	label: string;
	detail: string;
	/** A connection's why, or how the item is reached. */
	note?: string;
}

export interface MapSection {
	title: string;
	items: MapListItem[];
}

export interface MapView {
	target: MapTarget;
	/** Says what the map shows, for its heading. */
	title: string;
	center: string;
	nodes: MapNode[];
	edges: MapEdge[];
	/** The same data as lists (the "Show as list" switch). */
	sections: MapSection[];
	/** Something left out, said under the map. */
	note?: string;
}

export const frameNode = (key: string) => `f:${key}`;
export const nameNode = (id: string) => `n:${id}`;
export const subjectNode = (id: string) => `s:${id}`;

/**
 * The most frames reached through shared names in a two-step neighbourhood.
 * Sprint 018 measured a median of 22 frames one name away (p90 67, max 90):
 * uncapped, a Feynman frame's neighbourhood is the whole Feynman subject.
 */
export const SHARED_CAP = 8;

/** Past this many characters a label takes two lines. */
const LINE = 22;

/**
 * A label on the map, whole: one line when it is short, else two about as
 * long as each other, broken at a space. Never cut, and never inside a word.
 */
export function labelLines(s: string): string[] {
	if (s.length <= LINE) return [s];
	let best: string[] = [s];
	for (let i = s.indexOf(' '); i > 0; i = s.indexOf(' ', i + 1)) {
		const pair = [s.slice(0, i), s.slice(i + 1)];
		if (Math.max(...pair.map((l) => l.length)) < Math.max(...best.map((l) => l.length)))
			best = pair;
	}
	return best;
}
const plural = (n: number, one: string, many = `${one}s`) =>
	n === 0 ? `no ${many}` : `${n} ${n === 1 ? one : many}`;

export function viewOf(index: MapIndex, target: MapTarget): MapView | null {
	switch (target.view) {
		case 'frame':
			return index.frames.has(target.key) ? neighbourhood(index, target.key, target.steps) : null;
		case 'library':
			return library(index);
		case 'subject':
			return index.subjectTitles.has(target.id) ? subjectView(index, target.id) : null;
		case 'name':
			return index.data.names[target.id] ? nameView(index, target.id) : null;
	}
}

/** Builds a view's nodes and edges without repeating either. */
class Builder {
	nodes = new Map<string, MapNode>();
	edges = new Map<string, MapEdge>();
	constructor(readonly index: MapIndex) {}

	frame(key: string, ring: number, here = '') {
		const id = frameNode(key);
		if (!this.nodes.has(id)) {
			const f = this.index.frames.get(key)!;
			const s = subjectOf(key);
			this.nodes.set(id, {
				id,
				kind: 'frame',
				lines: labelLines(f.topic),
				full: f.topic,
				detail: [f.title, f.label, s === here ? null : this.index.subjectTitle(s)]
					.filter(Boolean)
					.join(' · '),
				subject: s,
				ring,
				size: ring === 0 ? 14 : 9
			});
		}
		return id;
	}

	name(id: string, ring: number) {
		const node = nameNode(id);
		if (!this.nodes.has(node)) {
			const n = this.index.data.names[id];
			const reach = this.index.reach(id);
			this.nodes.set(node, {
				id: node,
				kind: 'name',
				lines: labelLines(n.name),
				full: n.name,
				detail: `${n.kind}, in ${plural(reach, 'frame')}`,
				subject: null,
				ring,
				// Bigger as it reaches further, within bounds.
				size: ring === 0 ? 14 : Math.min(9, 4 + Math.sqrt(reach))
			});
		}
		return node;
	}

	edge(a: string, b: string, kind: MapEdgeKind, extra: Partial<MapEdge> = {}) {
		const [x, y] = a < b ? [a, b] : [b, a];
		const k = `${x} ${y}`;
		if (a !== b && !this.edges.has(k)) this.edges.set(k, { a: x, b: y, kind, weight: 1, ...extra });
	}

	/** Every connection between frames already on the map. */
	connectShown() {
		for (const l of this.index.data.links) {
			const a = frameNode(l.from);
			const b = frameNode(l.to);
			if (this.nodes.has(a) && this.nodes.has(b)) this.edge(a, b, 'connection', { why: l.why });
		}
	}

	/** A mention edge from each name on the map to each frame on it that marks the name. */
	mentionShown() {
		for (const node of this.nodes.values()) {
			if (node.kind !== 'name') continue;
			for (const key of this.index.data.mentions[node.id.slice(2)] ?? [])
				if (this.nodes.has(frameNode(key))) this.edge(node.id, frameNode(key), 'mention');
		}
	}

	item(node: string, note?: string): MapListItem {
		const n = this.nodes.get(node)!;
		return { node, label: n.full, detail: n.detail, ...(note ? { note } : {}) };
	}

	done(target: MapTarget, title: string, center: string, sections: MapSection[], note?: string) {
		return {
			target,
			title,
			center,
			nodes: [...this.nodes.values()],
			edges: [...this.edges.values()],
			sections: sections.filter((s) => s.items.length),
			...(note ? { note } : {})
		};
	}
}

const byKey = (a: string, b: string) => (a < b ? -1 : a > b ? 1 : 0);

/**
 * A frame's neighbourhood: the frame, its connections and the names it marks
 * (one step); then the connections of those, and the frames that share the
 * most telling names with it (two steps). A name marked in many frames tells
 * less about any one of them, so frames sharing names are ranked by the sum,
 * over the shared names, of one over the other frames each name is in, and
 * only the first `SHARED_CAP` are kept.
 */
function neighbourhood(index: MapIndex, key: string, steps: 1 | 2): MapView {
	const b = new Builder(index);
	const here = subjectOf(key);
	const center = b.frame(key, 0, here);
	const first = (index.connected.get(key) ?? []).slice().sort((x, y) => byKey(x.key, y.key));
	for (const c of first) b.frame(c.key, 1, here);
	const names = (index.marks.get(key) ?? []).slice();
	for (const id of names) b.name(id, 1);

	const second: { key: string; via: string; why: string }[] = [];
	let shared: { key: string; names: string[]; score: number }[] = [];
	if (steps === 2) {
		for (const c of first)
			for (const d of (index.connected.get(c.key) ?? [])
				.slice()
				.sort((x, y) => byKey(x.key, y.key)))
				if (!b.nodes.has(frameNode(d.key))) {
					b.frame(d.key, 2, here);
					second.push({ key: d.key, via: c.key, why: d.why });
				}
		const scores = new Map<string, { names: string[]; score: number }>();
		for (const id of names) {
			const at = index.data.mentions[id] ?? [];
			for (const other of at) {
				if (other === key) continue;
				const s = scores.get(other) ?? { names: [], score: 0 };
				s.names.push(id);
				s.score += 1 / (at.length - 1);
				scores.set(other, s);
			}
		}
		shared = [...scores]
			.map(([k, s]) => ({ key: k, ...s }))
			.sort((x, y) => y.score - x.score || byKey(x.key, y.key));
		for (const s of shared.slice(0, SHARED_CAP)) b.frame(s.key, 2, here);
	}
	b.connectShown();
	b.mentionShown();

	const f = index.frames.get(key)!;
	const kept = shared.slice(0, SHARED_CAP);
	const nameList = (ids: string[]) => ids.map((id) => index.data.names[id].name).join(', ');
	return b.done(
		{ view: 'frame', key, steps },
		`Around ${f.topic}`,
		center,
		[
			{
				title: 'Connections',
				items: first.map((c) => b.item(frameNode(c.key), c.why))
			},
			{
				title: 'Two steps away',
				items: second.map((s) =>
					b.item(frameNode(s.key), `Through ${index.frames.get(s.via)!.topic}: ${s.why}`)
				)
			},
			{
				title: 'Shares names',
				items: kept.map((s) => b.item(frameNode(s.key), `Shares ${nameList(s.names)}`))
			},
			{
				title: 'Names on this frame',
				items: names.map((id) => b.item(nameNode(id)))
			}
		],
		shared.length > SHARED_CAP
			? `${plural(shared.length - SHARED_CAP, 'more frame')} share a name with this one; the ${SHARED_CAP} sharing the rarest are shown.`
			: undefined
	);
}

/** Every subject, and how the subjects connect: the lines thicken with the connections. */
function library(index: MapIndex): MapView {
	const b = new Builder(index);
	const count = new Map<string, number>();
	for (const f of index.data.frames)
		count.set(subjectOf(f.key), (count.get(subjectOf(f.key)) ?? 0) + 1);
	const subjects = index.data.subjects;
	for (const s of subjects) {
		const n = count.get(s.id) ?? 0;
		b.nodes.set(subjectNode(s.id), {
			id: subjectNode(s.id),
			kind: 'subject',
			lines: labelLines(s.title),
			full: s.title,
			detail: plural(n, 'frame'),
			subject: s.id,
			ring: 0,
			size: 14 + Math.sqrt(n) * 2
		});
	}
	const pair = (a: string, c: string) => (a < c ? `${a} ${c}` : `${c} ${a}`);
	const links = new Map<string, number>();
	for (const l of index.data.links) {
		const [a, c] = [subjectOf(l.from), subjectOf(l.to)];
		if (a !== c) links.set(pair(a, c), (links.get(pair(a, c)) ?? 0) + 1);
	}
	const names = new Map<string, number>();
	for (const at of Object.values(index.data.mentions)) {
		const s = [...new Set(at.map(subjectOf))].sort(byKey);
		for (let i = 0; i < s.length; i++)
			for (let j = i + 1; j < s.length; j++)
				names.set(pair(s[i], s[j]), (names.get(pair(s[i], s[j])) ?? 0) + 1);
	}
	for (const [p, n] of links) {
		const [a, c] = p.split(' ');
		b.edge(subjectNode(a), subjectNode(c), 'between', { weight: n });
	}
	const joins = (id: string) =>
		subjects
			.filter((o) => o.id !== id)
			.map((o) => {
				const l = links.get(pair(id, o.id)) ?? 0;
				const n = names.get(pair(id, o.id)) ?? 0;
				return { o, l, n };
			})
			.filter((j) => j.l || j.n)
			.map(({ o, l, n }) => `${o.title}: ${plural(l, 'connection')}, ${plural(n, 'shared name')}`)
			.join('; ');
	return b.done({ view: 'library' }, 'The library', subjectNode(subjects[0]?.id ?? ''), [
		{
			title: 'Subjects',
			items: subjects.map((s) => b.item(subjectNode(s.id), joins(s.id) || 'No connections yet'))
		}
	]);
}

/** One subject's frames that have connections, and the frames they connect to. */
function subjectView(index: MapIndex, id: string): MapView {
	const b = new Builder(index);
	const center = subjectNode(id);
	const own = index.data.frames.filter((f) => subjectOf(f.key) === id);
	b.nodes.set(center, {
		id: center,
		kind: 'subject',
		lines: labelLines(index.subjectTitle(id)),
		full: index.subjectTitle(id),
		detail: plural(own.length, 'frame'),
		subject: id,
		ring: 0,
		size: 16
	});
	const linked = own.filter((f) => index.connected.has(f.key));
	for (const f of linked) b.frame(f.key, 1, id);
	const out: { key: string; from: string; why: string }[] = [];
	for (const f of linked)
		for (const c of index.connected.get(f.key)!)
			if (subjectOf(c.key) !== id) {
				b.frame(c.key, 2, id);
				out.push({ key: c.key, from: f.key, why: c.why });
			}
	b.connectShown();
	const title = index.subjectTitle(id);
	const others = [...new Set(out.map((o) => subjectOf(o.key)))];
	return b.done(
		{ view: 'subject', id },
		title,
		center,
		[
			{
				title: 'Frames with connections',
				items: linked.map((f) =>
					b.item(
						frameNode(f.key),
						index.connected
							.get(f.key)!
							.map((c) => index.frames.get(c.key)!.topic)
							.join('; ')
					)
				)
			},
			...others.map((o) => ({
				title: `In ${index.subjectTitle(o)}`,
				items: out
					.filter((x) => subjectOf(x.key) === o)
					.map((x) => b.item(frameNode(x.key), `From ${index.frames.get(x.from)!.topic}: ${x.why}`))
			}))
		],
		own.length > linked.length
			? `${plural(own.length - linked.length, 'frame')} of ${title} ${own.length - linked.length === 1 ? 'has' : 'have'} no connections yet, and ${own.length - linked.length === 1 ? 'is' : 'are'} left off.`
			: undefined
	);
}

/** One name in the middle, the frames that mark it around it: its card, as a graph. */
function nameView(index: MapIndex, id: string): MapView {
	const b = new Builder(index);
	const n = index.data.names[id];
	const center = b.name(id, 0);
	const at = index.data.mentions[id] ?? [];
	for (const key of at) b.edge(center, b.frame(key, 1), 'mention');
	b.connectShown();
	const bySubject = new Map<string, string[]>();
	for (const key of at)
		bySubject.set(subjectOf(key), [...(bySubject.get(subjectOf(key)) ?? []), key]);
	return b.done({ view: 'name', id }, n.name, center, [
		...(n.home ? [{ title: 'Chiefly', items: [b.item(frameNode(n.home))] }] : []),
		...[...bySubject].map(([s, keys]) => ({
			title: `In ${index.subjectTitle(s)}`,
			items: keys.filter((k) => k !== n.home).map((k) => b.item(frameNode(k)))
		}))
	]);
}

// ---------------------------------------------------------------------------
// Layout: seeded, and run to rest before it is drawn.

export interface Point {
	x: number;
	y: number;
}

/** A small seeded generator (mulberry32), so a layout never depends on Math.random. */
export function seeded(seed: string): () => number {
	let h = 1779033703 ^ seed.length;
	for (let i = 0; i < seed.length; i++) {
		h = Math.imul(h ^ seed.charCodeAt(i), 3432918353);
		h = (h << 13) | (h >>> 19);
	}
	let a = h >>> 0;
	return () => {
		a = (a + 0x6d2b79f5) | 0;
		let t = Math.imul(a ^ (a >>> 15), 1 | a);
		t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}

type SimNode = SimulationNodeDatum & { id: string; ring: number; size: number };

/** How far apart the rings sit, in layout units. */
const RING = 150;
/** The room a node wants along its ring. */
const SPACING = 48;
const TICKS = 300;

/**
 * Where each node goes. The centre is pinned at the origin; the rest start
 * on their rings, grouped by subject, and settle under a force layout that
 * keeps them apart and near their ring. A ring widens with its nodes, so a
 * subject's forty frames do not crowd the one ring they share. Same view in,
 * same places out.
 */
export function layoutView(view: MapView): Map<string, Point> {
	const radial = view.target.view !== 'library';
	const rings = new Map<number, MapNode[]>();
	const order = (n: MapNode) => `${n.kind === 'name' ? '1' : '0'} ${n.subject ?? ''} ${n.id}`;
	for (const n of [...view.nodes].sort((a, b) => byKey(order(a), order(b))))
		rings.set(n.ring, [...(rings.get(n.ring) ?? []), n]);
	// A ring is wide enough for its nodes to stand apart, and outside the one within it.
	const radius = new Map<number, number>([[0, 0]]);
	for (const ring of [...rings.keys()].sort((a, b) => a - b))
		if (ring > 0)
			radius.set(
				ring,
				Math.max(
					(radius.get(ring - 1) ?? 0) + RING,
					(rings.get(ring)!.length * SPACING) / (2 * Math.PI)
				)
			);
	const nodes: SimNode[] = [];
	for (const [ring, members] of rings)
		members.forEach((n, i) => {
			const angle = (2 * Math.PI * i) / members.length - Math.PI / 2;
			const r = radial ? radius.get(ring)! : RING * 1.5;
			const pinned = n.id === view.center && radial;
			nodes.push({
				id: n.id,
				ring: n.ring,
				size: n.size,
				x: pinned ? 0 : Math.cos(angle) * r,
				y: pinned ? 0 : Math.sin(angle) * r,
				...(pinned ? { fx: 0, fy: 0 } : {})
			});
		});
	const links: SimulationLinkDatum<SimNode>[] = view.edges.map((e) => ({
		source: e.a,
		target: e.b
	}));
	const sim = forceSimulation(nodes)
		.randomSource(seeded(JSON.stringify(view.target)))
		.force(
			'link',
			forceLink<SimNode, SimulationLinkDatum<SimNode>>(links)
				.id((n) => n.id)
				.distance(radial ? RING * 0.9 : RING * 2)
				.strength(radial ? 0.05 : 0.2)
		)
		.force('charge', forceManyBody<SimNode>().strength(radial ? -160 : -900))
		.force(
			'collide',
			forceCollide<SimNode>().radius((n) => n.size + 16)
		)
		.stop();
	if (radial)
		sim.force(
			'ring',
			forceRadial<SimNode>((n) => radius.get(n.ring)!).strength((n) => (n.ring ? 0.6 : 0))
		);
	sim.tick(TICKS);
	return new Map(
		nodes.map((n) => [n.id, { x: Math.round(n.x! * 10) / 10, y: Math.round(n.y! * 10) / 10 }])
	);
}

/** The box the layout covers, with each node's size. */
export function extent(view: MapView, at: Map<string, Point>) {
	let [x0, y0, x1, y1] = [Infinity, Infinity, -Infinity, -Infinity];
	for (const n of view.nodes) {
		const p = at.get(n.id)!;
		x0 = Math.min(x0, p.x - n.size);
		y0 = Math.min(y0, p.y - n.size);
		x1 = Math.max(x1, p.x + n.size);
		y1 = Math.max(y1, p.y + n.size);
	}
	return { x0, y0, x1, y1 };
}

// ---------------------------------------------------------------------------
// Labels: placed where they fit, in order of importance; the rest wait for focus.

export type LabelSide = 'right' | 'left' | 'above' | 'below';

export interface LabelBox {
	id: string;
	/** On screen, in pixels. */
	x: number;
	y: number;
	r: number;
	width: number;
	height: number;
	/** Placed first when higher. */
	priority: number;
}

interface Rect {
	x0: number;
	y0: number;
	x1: number;
	y1: number;
}

const overlaps = (a: Rect, b: Rect) => a.x0 < b.x1 && b.x0 < a.x1 && a.y0 < b.y1 && b.y0 < a.y1;

function sideRect(l: LabelBox, side: LabelSide): Rect {
	const gap = 4;
	switch (side) {
		case 'right':
			return {
				x0: l.x + l.r + gap,
				y0: l.y - l.height / 2,
				x1: l.x + l.r + gap + l.width,
				y1: l.y + l.height / 2
			};
		case 'left':
			return {
				x0: l.x - l.r - gap - l.width,
				y0: l.y - l.height / 2,
				x1: l.x - l.r - gap,
				y1: l.y + l.height / 2
			};
		case 'above':
			return {
				x0: l.x - l.width / 2,
				y0: l.y - l.r - gap - l.height,
				x1: l.x + l.width / 2,
				y1: l.y - l.r - gap
			};
		case 'below':
			return {
				x0: l.x - l.width / 2,
				y0: l.y + l.r + gap,
				x1: l.x + l.width / 2,
				y1: l.y + l.r + gap + l.height
			};
	}
}

/**
 * Where each label goes: right of its node, else left, above or below,
 * wherever it hits no label placed before it, no node and no edge of the
 * area. A label that fits nowhere is null, and shows when its node has focus
 * or the pointer.
 */
export function placeLabels(
	labels: LabelBox[],
	area: { width: number; height: number }
): Map<string, LabelSide | null> {
	const placed: Rect[] = [];
	const dots: (Rect & { id: string })[] = labels.map((l) => ({
		id: l.id,
		x0: l.x - l.r,
		y0: l.y - l.r,
		x1: l.x + l.r,
		y1: l.y + l.r
	}));
	const out = new Map<string, LabelSide | null>();
	const inside = (r: Rect) => r.x0 >= 0 && r.y0 >= 0 && r.x1 <= area.width && r.y1 <= area.height;
	for (const l of [...labels].sort((a, b) => b.priority - a.priority || byKey(a.id, b.id))) {
		let chosen: LabelSide | null = null;
		for (const side of ['right', 'left', 'above', 'below'] as const) {
			const r = sideRect(l, side);
			if (
				inside(r) &&
				!placed.some((p) => overlaps(p, r)) &&
				!dots.some((d) => d.id !== l.id && overlaps(d, r))
			) {
				chosen = side;
				placed.push(r);
				break;
			}
		}
		out.set(l.id, chosen);
	}
	return out;
}

// ---------------------------------------------------------------------------
// Keys: an arrow moves to the neighbour that lies that way.

export type Direction = 'up' | 'down' | 'left' | 'right';

const ANGLE: Record<Direction, number> = {
	right: 0,
	down: Math.PI / 2,
	left: Math.PI,
	up: -Math.PI / 2
};

/**
 * The node an arrow key moves to from `from`: among the nodes joined to it,
 * the nearest one that lies within 67.5° of the arrow's way, turning counting
 * against it; when none is joined that way, the nearest node of all that
 * lies that way. Null at the edge of the map.
 */
export function stepFrom(
	view: MapView,
	at: Map<string, Point>,
	from: string,
	direction: Direction
): string | null {
	const p = at.get(from);
	if (!p) return null;
	const joined = new Set<string>();
	for (const e of view.edges) {
		if (e.a === from) joined.add(e.b);
		if (e.b === from) joined.add(e.a);
	}
	const want = ANGLE[direction];
	const best = (ids: Iterable<string>) => {
		let pick: string | null = null;
		let score = Infinity;
		for (const id of ids) {
			if (id === from) continue;
			const q = at.get(id);
			if (!q) continue;
			const dx = q.x - p.x;
			const dy = q.y - p.y;
			const dist = Math.hypot(dx, dy);
			if (!dist) continue;
			let turn = Math.abs(Math.atan2(dy, dx) - want);
			if (turn > Math.PI) turn = 2 * Math.PI - turn;
			if (turn > (3 * Math.PI) / 8) continue;
			const s = dist * (1 + 2 * turn);
			if (s < score || (s === score && pick !== null && id < pick)) {
				score = s;
				pick = id;
			}
		}
		return pick;
	};
	return best(joined) ?? best(view.nodes.map((n) => n.id));
}

// ---------------------------------------------------------------------------
// Subjects: a colour and a shape each, in the order the app serves them.

/**
 * The shapes a subject's frames wear on the map, in slot order. Colour alone
 * cannot tell four subjects apart on every palette (sprint 019), so a shape
 * always goes with it, and the legend names both.
 */
export const SHAPES = ['circle', 'square', 'diamond', 'triangle', 'hexagon', 'star'] as const;
export type Shape = (typeof SHAPES)[number] | 'other';

/** A subject's slot: its colour (`--map-s<slot>`) and its shape. Past the last, both are "other". */
export function subjectSlot(data: MapData, id: string): { slot: number | null; shape: Shape } {
	const i = data.subjects.findIndex((s) => s.id === id);
	return i >= 0 && i < SHAPES.length
		? { slot: i + 1, shape: SHAPES[i] }
		: { slot: null, shape: 'other' };
}
