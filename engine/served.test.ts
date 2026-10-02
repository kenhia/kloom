import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { loadSubject } from './load';
import type { Subject } from './model';
import { around, bodyOf, headOf, subjectHeadOf } from './served';

let subject: Subject;
beforeAll(async () => {
	subject = await loadSubject(join(import.meta.dirname, '..', 'subjects', 'western-civ'));
});

describe('a served subject', () => {
	it('splits a frame into a head and a body that make it whole again', () => {
		const f = subject.frames.prometheus;
		const head = headOf(f);
		expect(Object.keys(head)).not.toEqual(expect.arrayContaining(['readingHtml']));
		expect({ ...head, ...bodyOf(f) }).toEqual(f);
		expect(subjectHeadOf(subject).frames.writing).toEqual(headOf(subject.frames.writing));
	});

	it('names the frames around one, nearest first, on the spine that walks it', () => {
		const head = subjectHeadOf(subject);
		expect(around(head, 'greek-inquiry')).toEqual([
			'greek-inquiry',
			'eratosthenes',
			'writing',
			'pantheon',
			'prometheus'
		]);
		// At the start of the spine, only what is there.
		expect(around(head, 'prometheus')).toEqual(['prometheus', 'writing', 'greek-inquiry']);
		// A trail's frame, on its trail.
		expect(around(head, 'royal-cubit', 1)).toEqual(['royal-cubit', 'harrison-chronometer']);
		expect(around(head, 'nope')).toEqual([]);
	});
});
