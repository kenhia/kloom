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
		sources: [
			{ title: 'Press article', url: 'https://example.org/press' },
			{ title: 'A book with no link' }
		],
		citations: [cite('Press article', 'https://example.org/press'), cite('Ink', 'https://ink.test')]
	},
	trail: null
};
