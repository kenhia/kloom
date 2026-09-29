import { describe, expect, it } from 'vitest';
import { ASK_MODEL, GROW_MODEL } from '../settings';
import { aiVerbs, isGrow } from './control';

describe('the AI control', () => {
	it('puts "Ask a question" first, then the grow verbs', () => {
		expect(aiVerbs(true).map((v) => v.value)).toEqual(['ask', 'frames', 'trail', 'both']);
		expect(aiVerbs(true)[0].label).toBe('Ask a question');
	});

	it('offers only ask when grow is not configured', () => {
		expect(aiVerbs(false).map((v) => v.value)).toEqual(['ask']);
	});

	it('sends a question with the ask model, and grows with the grow model', () => {
		const [ask, ...grow] = aiVerbs(true);
		expect(ask).toMatchObject({ send: 'Ask', model: ASK_MODEL });
		for (const v of grow) expect(v).toMatchObject({ send: 'Grow', model: GROW_MODEL });
	});

	it('tells ask from grow', () => {
		expect(isGrow('ask')).toBe(false);
		for (const v of ['frames', 'trail', 'both'] as const) expect(isGrow(v)).toBe(true);
	});

	it('gives every verb its own placeholder', () => {
		const placeholders = aiVerbs(true).map((v) => v.placeholder);
		expect(new Set(placeholders).size).toBe(placeholders.length);
	});
});
