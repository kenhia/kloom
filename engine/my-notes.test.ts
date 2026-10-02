import { describe, expect, it } from 'vitest';
import {
	annotatedFrames,
	bySubject,
	clearQuestion,
	detachedIn,
	filterCounts,
	isLive,
	keeps,
	statesOf,
	type NoteEntry
} from './my-notes';

const entry = (over: Partial<NoteEntry>): NoteEntry => ({
	id: 'n',
	subject: 'ai',
	frame: 'turing',
	label: 'Turing',
	text: 'a note',
	anchor: null,
	review: 'none',
	response: null,
	unseen: false,
	created: '2026-10-01T00:00:00.000Z',
	updated: '2026-10-01T00:00:00.000Z',
	subjectTitle: 'Artificial Intelligence',
	topic: 'the Turing test',
	position: '1950',
	...over
});

const words = { exact: 'the imitation game', prefix: 'He called it ', suffix: ', and', start: 13 };
const plain = entry({ id: 'plain' });
const pending = entry({ id: 'pending', review: 'flagged' });
const answered = entry({ id: 'answered', review: 'handled', response: 'Fixed.', unseen: true });
const lost = entry({ id: 'lost', anchor: words, review: 'handled', response: 'Reworded.' });
const found = entry({ id: 'found', anchor: words });
const detached = new Set(['lost']);

describe('a note’s state', () => {
	it('is said in words, and may be answered and detached at once', () => {
		expect(statesOf(plain, detached)).toEqual([]);
		expect(statesOf(pending, detached)).toEqual(['Agent review (pending)']);
		expect(statesOf(answered, detached)).toEqual(['Answered (new)']);
		expect(statesOf(lost, detached)).toEqual(['Answered', 'Detached']);
		expect(statesOf(found, detached)).toEqual([]);
	});

	it('decides what each filter keeps, and counts them', () => {
		const all = [plain, pending, answered, lost, found];
		const kept = (f: Parameters<typeof keeps>[0]) =>
			all.filter((n) => keeps(f, n, detached)).map((n) => n.id);
		expect(kept('all')).toHaveLength(5);
		expect(kept('pending')).toEqual(['pending']);
		expect(kept('answered')).toEqual(['answered', 'lost']);
		expect(kept('detached')).toEqual(['lost']);
		expect(filterCounts(all, detached)).toEqual({ all: 5, pending: 1, answered: 2, detached: 1 });
	});

	it('can be gone to only while its subject and frame are served', () => {
		expect(isLive(plain)).toBe(true);
		expect(isLive(entry({ topic: null, position: null }))).toBe(false);
		expect(isLive(entry({ subjectTitle: null, topic: null }))).toBe(false);
	});
});

describe('the list', () => {
	it('groups by subject, in the order of each subject’s newest note', () => {
		const notes = [
			entry({ id: 'a', subject: 'ai' }),
			entry({ id: 'b', subject: 'feynman', subjectTitle: 'Feynman' }),
			entry({ id: 'c', subject: 'ai' }),
			entry({ id: 'd', subject: 'gone', subjectTitle: null, topic: null })
		];
		expect(bySubject(notes).map((g) => [g.title, g.notes.map((n) => n.id)])).toEqual([
			['Artificial Intelligence', ['a', 'c']],
			['Feynman', ['b']],
			['gone', ['d']]
		]);
	});
});

describe('detached annotations', () => {
	it('are looked for frame by frame', () => {
		const other = entry({ id: 'other', frame: 'eliza', anchor: words });
		expect(annotatedFrames([plain, found, other, lost]).map((f) => f.map((n) => n.id))).toEqual([
			['found', 'lost'],
			['other']
		]);
	});

	it('are the ones whose words the reading no longer has', () => {
		const text = 'He called it   the imitation\ngame, and it stuck.';
		expect(detachedIn(text, [plain, found, lost])).toEqual([]);
		expect(detachedIn('He called it a parlour game, and it stuck.', [plain, found])).toEqual([
			'found'
		]);
	});
});

describe('the bulk clears', () => {
	it('say how many they will delete', () => {
		expect(clearQuestion('answered', 3)).toBe(
			'Delete all 3 answered notes? This cannot be undone.'
		);
		expect(clearQuestion('detached', 1)).toBe(
			'Delete the detached annotation? This cannot be undone.'
		);
	});
});
