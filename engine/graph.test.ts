import { describe, expect, it } from 'vitest';
import { buildGraph, graphProblems, linksByFrame, nameCard, type GraphSubject } from './graph';
import type { Name } from './names';

const frame = (
	subject: string,
	id: string,
	extra: Partial<GraphSubject['frames'][number]> = {}
): GraphSubject['frames'][number] => ({
	subject,
	frame: id,
	title: `We did ${id.toUpperCase()}`,
	topic: `Topic ${id}`,
	label: id,
	trail: null,
	connections: [],
	names: [],
	...extra
});

const subjects = (): GraphSubject[] => [
	{
		id: 'ai',
		title: 'AI',
		frames: [
			frame('ai', 'turing-machine', {
				names: ['alan-turing'],
				connections: [{ to: 'computing/edvac', why: 'The stored program.' }]
			}),
			frame('ai', 'turing-test', { names: ['alan-turing'] })
		]
	},
	{
		id: 'computing',
		title: 'Computing',
		frames: [
			frame('computing', 'edvac'),
			frame('computing', 'bombe', {
				names: ['alan-turing', 'bletchley'],
				trail: 'Codebreaking',
				connections: [
					{ to: 'ai/turing-test', why: 'Turing, before the game.' },
					{ to: 'feynman/gone', why: 'A subject not served.' }
				]
			})
		]
	}
];

const names: Record<string, Name> = {
	'alan-turing': {
		id: 'alan-turing',
		wikidata: 'Q7251',
		name: 'Alan Turing',
		kind: 'person',
		description: 'Mathematician.',
		home: 'ai/turing-machine'
	}
};

describe('the graph', () => {
	const graph = buildGraph(subjects(), names);
	const links = linksByFrame(graph);
	const on = (key: string) => links.get(key)!.connections;

	it('shows a connection on both frames, with its why', () => {
		expect(on('ai/turing-machine')).toEqual([
			{
				direction: 'out',
				why: 'The stored program.',
				subject: 'computing',
				subjectTitle: 'Computing',
				frame: 'edvac',
				title: 'We did EDVAC',
				topic: 'Topic edvac',
				label: 'edvac',
				trail: null,
				detached: false
			}
		]);
		expect(on('ai/turing-test')).toEqual([
			expect.objectContaining({
				direction: 'in',
				frame: 'bombe',
				trail: 'Codebreaking',
				why: 'Turing, before the game.'
			})
		]);
		expect(on('computing/edvac')).toEqual([
			expect.objectContaining({ direction: 'in', subject: 'ai', frame: 'turing-machine' })
		]);
	});

	it('shows a connection to a frame that is not there as detached', () => {
		expect(on('computing/bombe')[1]).toEqual({
			direction: 'out',
			why: 'A subject not served.',
			subject: 'feynman',
			subjectTitle: 'feynman',
			frame: 'gone',
			detached: true
		});
	});

	it("puts a name's home first, then the reader's subject, then the others", () => {
		const card = nameCard(graph, 'alan-turing', 'computing')!;
		expect(card.home?.frame).toBe('turing-machine');
		expect(card.groups.map((g) => [g.subject, g.entries.map((e) => e.frame)])).toEqual([
			['computing', ['bombe']],
			['ai', ['turing-test']]
		]);
		expect(nameCard(graph, 'alan-turing', 'ai')!.groups[0].subject).toBe('ai');
	});

	it("gives a frame the cards of the names it marks, and only the registry's", () => {
		expect(Object.keys(links.get('computing/bombe')!.names)).toEqual(['alan-turing']);
		expect(links.get('computing/bombe')!.names['alan-turing'].groups[0].subject).toBe('computing');
		expect(links.get('computing/edvac')).toEqual({ connections: [expect.anything()], names: {} });
		expect(nameCard(graph, 'bletchley', 'computing')).toBeNull();
	});

	it('names what the gate refuses: missing targets, pairs stored twice, unknown names', () => {
		const s = subjects();
		s[0].frames[1].connections = [{ to: 'computing/bombe', why: 'Stored on both ends.' }];
		s[0].frames[0].connections.push({ to: 'ai/turing-machine', why: 'Itself.' });
		const g = buildGraph(s, { ...names, x: { ...names['alan-turing'], id: 'x', home: 'ai/no' } });
		expect(graphProblems(g)).toEqual([
			'ai/turing-machine: connects to itself',
			'computing/bombe: ai/turing-test already connects to it; store a connection on one end',
			'computing/bombe: connects to feynman/gone, not a frame',
			'names/x.json: home ai/no is not a frame',
			'computing/bombe: marks "bletchley", not in the name registry'
		]);
	});
});
