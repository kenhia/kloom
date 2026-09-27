import type { Citation } from '$engine/citation';

/**
 * The start screen's loom: traced from a public-domain engraving
 * (see README.md in this directory for how, and the file page's terms).
 */
export const loomCredit: Citation = {
	kind: 'media',
	title: 'Modern Loose Reed Power Loom',
	url: 'https://commons.wikimedia.org/wiki/File:Modern_Loose_Reed_Power_Loom-marsden.png',
	accessed: '2026-09-26',
	authors: [{ family: 'Marsden', given: 'Richard' }],
	published: '1895',
	container:
		'In Cotton Weaving: Its Development, Principles, and Practice (London: George Bell & Sons); via Wikimedia Commons',
	licence: 'Public domain',
	file: 'loom.svg'
};

export const inscription = 'KLOOM · A LOOM FOR WHAT WE KNOW · WEAVE A THREAD · ';
