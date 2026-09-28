import type { Citation } from '../model';
import type { AskContext } from './provider';

/** A small ask context shared by the ask tests. */
const cite = (title: string, url: string): Citation => ({
	kind: 'web',
	title,
	url,
	accessed: '2026-09-26'
});

export const context: AskContext = {
	subject: { title: 'A Subject' },
	frame: {
		id: 'press',
		title: 'We printed WORDS.',
		position: 'AD 1440',
		segment: 'Renaissance',
		reading: 'Gutenberg built a press.\n',
		citations: [
			{ ...cite('Press article', 'https://example.org/press'), key: true },
			cite('Ink', 'https://ink.test'),
			{ kind: 'book', title: 'A book with a DOI', doi: '10.1000/xyz', accessed: '2026-09-26' }
		]
	},
	trail: null
};
