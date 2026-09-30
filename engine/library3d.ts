import { subjectOf, type MapData } from './map';

/**
 * The library in 3D (docs/design.md §The library in 3D, korg 3449): every
 * frame and name and every connection, for a WebGL force graph you can turn
 * and fly through. This file decides what is drawn and what the text summary
 * says; engine/ui/Library3d.svelte hands it to `3d-force-graph`.
 *
 * It is decorative. The 2D map and its list stay the way to read the graph,
 * so nothing here has to be reachable by keyboard, only counted in words.
 */

export interface Node3d {
	/** `f:<subject>/<frame>` or `n:<name>`, as on the 2D map. */
	id: string;
	kind: 'frame' | 'name';
	/** The frame's subject; null for a name, which belongs to none. */
	subject: string | null;
	/** Its name on the graph: a frame's topic, a name's name. */
	label: string;
	/** Said under the label: a frame's title, subject and position; a name's description. */
	detail: string;
	/** How many links it has here, to size it. */
	degree: number;
}

export interface Link3d {
	source: string;
	target: string;
	/** A connection between two frames, or a frame marking a name. */
	kind: 'connection' | 'mention';
}

/** One subject's share of the graph, for the text summary. */
export interface SubjectCounts {
	id: string;
	title: string;
	frames: number;
	/** Connections with an end here; one between two subjects counts in both. */
	connections: number;
	/** Distinct names its frames mark. */
	names: number;
}

export interface Library3d {
	nodes: Node3d[];
	links: Link3d[];
	subjects: SubjectCounts[];
	totals: { frames: number; names: number; connections: number; mentions: number };
}

export function library3dOf(data: MapData): Library3d {
	const titles = new Map(data.subjects.map((s) => [s.id, s.title]));
	const degree = new Map<string, number>();
	const bump = (id: string) => degree.set(id, (degree.get(id) ?? 0) + 1);

	const links: Link3d[] = [];
	for (const l of data.links) {
		links.push({ source: `f:${l.from}`, target: `f:${l.to}`, kind: 'connection' });
		bump(`f:${l.from}`);
		bump(`f:${l.to}`);
	}
	for (const [name, at] of Object.entries(data.mentions)) {
		if (!data.names[name]) continue;
		for (const key of at) {
			links.push({ source: `f:${key}`, target: `n:${name}`, kind: 'mention' });
			bump(`f:${key}`);
			bump(`n:${name}`);
		}
	}

	const nodes: Node3d[] = [
		...data.frames.map((f): Node3d => {
			const subject = subjectOf(f.key);
			return {
				id: `f:${f.key}`,
				kind: 'frame',
				subject,
				label: f.topic,
				detail: [
					f.title,
					titles.get(subject) ?? subject,
					f.trail ? `${f.label}, ${f.trail}` : f.label
				]
					.filter(Boolean)
					.join(' · '),
				degree: degree.get(`f:${f.key}`) ?? 0
			};
		}),
		...Object.entries(data.names)
			.filter(([id]) => data.mentions[id]?.length)
			.map(([id, n]): Node3d => ({
				id: `n:${id}`,
				kind: 'name',
				subject: null,
				label: n.name,
				detail: n.description,
				degree: degree.get(`n:${id}`) ?? 0
			}))
	];

	const subjects = data.subjects.map((s): SubjectCounts => {
		const mine = (key: string) => subjectOf(key) === s.id;
		const names = new Set(
			Object.entries(data.mentions)
				.filter(([id, at]) => data.names[id] && at.some(mine))
				.map(([id]) => id)
		);
		return {
			id: s.id,
			title: s.title,
			frames: data.frames.filter((f) => mine(f.key)).length,
			connections: data.links.filter((l) => mine(l.from) || mine(l.to)).length,
			names: names.size
		};
	});

	return {
		nodes,
		links,
		subjects,
		totals: {
			frames: data.frames.length,
			names: nodes.length - data.frames.length,
			connections: data.links.length,
			mentions: links.length - data.links.length
		}
	};
}
