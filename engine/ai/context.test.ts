import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { loadSubject } from '../load';
import type { Subject } from '../model';
import { askContext } from './context';

let subject: Subject;
beforeAll(async () => {
	subject = await loadSubject(join(import.meta.dirname, '..', '..', 'subjects', 'western-civ'));
});

const none = { reading: '', citations: [] };

describe('the ask context', () => {
	it('is built from the subject for a main-spine frame', () => {
		const { citations } = subject.frames['printing-press'];
		const c = askContext(subject, 'printing-press', null, { reading: 'the reading', citations })!;
		expect(c.subject.title).toBe(subject.title);
		expect(c.frame.id).toBe('printing-press');
		expect(c.frame.reading).toBe('the reading');
		expect(c.frame.citations).toBe(citations);
		expect(c.trail).toBeNull();
	});

	it('names the trail, and its segment, for a trail frame', () => {
		const c = askContext(subject, 'gutenberg-bible', 'printing', none)!;
		expect(c.trail).toEqual({ id: 'printing', title: 'The printing press' });
		expect(c.frame.segment).toBe('Mainz');
	});

	it('refuses an unknown frame, an unknown trail, or a trail that does not hold the frame', () => {
		expect(askContext(subject, 'nope', null, none)).toBeNull();
		expect(askContext(subject, '__proto__', null, none)).toBeNull();
		expect(askContext(subject, 'printing-press', 'nope', none)).toBeNull();
		expect(askContext(subject, 'printing-press', 'printing', none)).toBeNull();
		expect(askContext(subject, 'gutenberg-bible', null, none)).toBeNull();
	});
});
