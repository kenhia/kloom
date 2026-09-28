import { describe, expect, it } from 'vitest';
import { ANSWER_ID, answerId, keptAnswer, keptAnswerProblems, type Answer } from './kept';
import { context } from './fixture';

const answer: Answer = {
	id: answerId(new Date('2026-09-27T17:05:09.123Z'), '0a1b2c3d'),
	subject: 'western-civ',
	context: { ...context, trail: { id: 'ink', title: 'Ink' } },
	question: 'Why?',
	answer: 'Because of ink [2] and a book [3].',
	provider: 'claude-cli',
	model: 'claude-sonnet-5',
	askedAt: '2026-09-27T17:05:09.123Z'
};

describe('kept answers', () => {
	it('names an answer by when it was asked, safely for a file name', () => {
		expect(answer.id).toBe('20260927T170509Z-0a1b2c3d');
		expect(ANSWER_ID.test(answer.id)).toBe(true);
		expect(ANSWER_ID.test('../../etc/passwd')).toBe(false);
	});

	it('carries the anchor, the answer and exactly the references it marked', () => {
		const kept = keptAnswer(answer, new Date('2026-09-27T17:06:00Z'));
		expect(kept).toMatchObject({
			kind: 'kloom.kept-answer',
			version: 1,
			anchor: { frame: 'press', trail: 'ink' },
			answer: answer.answer,
			keptAt: '2026-09-27T17:06:00.000Z'
		});
		expect(kept.citations.map((c) => c.title)).toEqual(['Ink', 'A book with a DOI']);
		// Sources are key citations now (sprint 008); the field stays, empty, for version 1.
		expect(kept.sources).toEqual([]);
		expect(keptAnswerProblems(kept)).toEqual([]);
	});

	it('finds what is wrong with a malformed file', () => {
		const kept = keptAnswer(answer, new Date());
		expect(keptAnswerProblems({ ...kept, version: 2, id: 'x' })).toEqual([
			'version must be 1',
			'id is malformed'
		]);
		expect(keptAnswerProblems({ ...kept, anchor: { frame: 'press' } })).toEqual([
			'anchor.trail must be a trail id or null'
		]);
		expect(keptAnswerProblems({ ...kept, citations: [{ title: 'x' }] })[0]).toMatch(
			/^citations\[0\]/
		);
		expect(keptAnswerProblems(null)).toEqual(['not an object']);
	});
});
