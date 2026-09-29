import { describe, expect, it } from 'vitest';
import { buildNames, nameProblems } from './names';

const turing = {
	id: 'alan-turing',
	wikidata: 'Q7251',
	name: 'Alan Turing',
	kind: 'person',
	description: 'English mathematician; computability, codebreaking and the imitation game.',
	home: 'ai/turing-machine'
};

describe('nameProblems', () => {
	it('accepts a well-formed name, and one with no Wikidata item', () => {
		expect(nameProblems('alan-turing', turing)).toEqual([]);
		expect(nameProblems('x', { ...turing, id: 'x', wikidata: null, home: undefined })).toEqual([]);
	});

	it('says everything wrong with a name at once', () => {
		expect(
			nameProblems('Bad_Id', {
				id: 'other',
				wikidata: '7251',
				kind: 'wizard',
				aliases: 'Turing',
				home: 'turing-machine'
			})
		).toEqual([
			'"Bad_Id" is not a name id (lower case, digits, -)',
			'id must match the file name ("Bad_Id")',
			'wikidata must be a Wikidata item id (Q…) or null',
			'name is required',
			'kind must be one of person, place, org, artifact, idea, event',
			'description is required',
			'aliases must be a list of strings',
			'home must be "<subject>/<frame>"'
		]);
	});

	it('requires wikidata to be said, even as null', () => {
		const without: Partial<typeof turing> = { ...turing };
		delete without.wikidata;
		expect(nameProblems('alan-turing', without)).toContain(
			'wikidata must be a Wikidata item id (Q…) or null'
		);
	});
});

describe('buildNames', () => {
	it('keeps the valid names and names every problem', () => {
		const { names, problems } = buildNames({
			'alan-turing': turing,
			turing: { ...turing, id: 'turing' },
			broken: { id: 'broken' }
		});
		expect(Object.keys(names)).toEqual(['alan-turing', 'turing']);
		expect(problems).toEqual([
			'names/turing.json: Q7251 is already names/alan-turing',
			'names/broken.json: wikidata must be a Wikidata item id (Q…) or null',
			'names/broken.json: name is required',
			'names/broken.json: kind must be one of person, place, org, artifact, idea, event',
			'names/broken.json: description is required'
		]);
	});
});
