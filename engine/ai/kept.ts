import { citationProblems } from '../citation';
import type { Citation, Source } from '../model';
import { citedNumbers, references } from './prompt';
import type { AskContext } from './provider';

/**
 * A kept answer: what "keep this" stores, and what grow (korg 3364) consumes
 * as a candidate addition. It is not subject content. One JSON file per
 * answer, under the app's data directory (docs/design.md §Ask).
 */
export interface KeptAnswer {
	kind: 'kloom.kept-answer';
	version: 1;
	id: string;
	/** The subject's directory name, e.g. "western-civ". */
	subject: string;
	/** Where it was asked: the frame, and the trail if the reader was on one. */
	anchor: { frame: string; trail: string | null };
	question: string;
	/** Markdown, exactly as the model wrote it, `[n]` markers and all. */
	answer: string;
	/** The frame's citations the answer marked, in first-use order. */
	citations: Citation[];
	/**
	 * Before sprint 008, the frame's plain sources the answer marked. A frame's
	 * sources are now its key citations, so this is always empty; it stays so
	 * the format, and the files already kept, remain version 1.
	 */
	sources: Source[];
	/**
	 * The web pages a web turn listed (`[W1] Title — URL`), as `web`
	 * citations, or as `wikipedia` ones pinned to a revision. Absent when the
	 * turn did not use the web. Added in sprint 005 (korg 3376); optional, so
	 * the format stays version 1.
	 */
	webCitations?: Citation[];
	provider: string;
	model: string;
	/** ISO 8601 UTC. */
	askedAt: string;
	keptAt: string;
}

/** A finished answer, as the server remembers it until it is kept or forgotten. */
export interface Answer {
	id: string;
	subject: string;
	context: AskContext;
	question: string;
	answer: string;
	provider: string;
	model: string;
	askedAt: string;
	/** Whether the turn was allowed the web. */
	web?: boolean;
}

export function keptAnswer(a: Answer, keptAt: Date, webCitations?: Citation[]): KeptAnswer {
	const refs = references(a.context.frame);
	const used = citedNumbers(a.answer, refs.length).map((n) => refs[n - 1]);
	return {
		kind: 'kloom.kept-answer',
		version: 1,
		id: a.id,
		subject: a.subject,
		anchor: { frame: a.context.frame.id, trail: a.context.trail?.id ?? null },
		question: a.question,
		answer: a.answer,
		citations: used.map((r) => r.citation),
		sources: [],
		...(webCitations ? { webCitations } : {}),
		provider: a.provider,
		model: a.model,
		askedAt: a.askedAt,
		keptAt: keptAt.toISOString()
	};
}

/** An answer id: when it was asked, and a random tail. Safe as a file name. */
export const ANSWER_ID = /^\d{8}T\d{6}Z-[0-9a-f]{8}$/;

export function answerId(at: Date, random: string): string {
	return `${at
		.toISOString()
		.replace(/[-:]/g, '')
		.replace(/\.\d+Z$/, 'Z')}-${random}`;
}

const str = (v: unknown) => typeof v === 'string' && v.trim() !== '';

/** Every problem with a kept-answer file, for grow to check before it reads one. */
export function keptAnswerProblems(x: unknown): string[] {
	if (typeof x !== 'object' || x === null) return ['not an object'];
	const k = x as Record<string, unknown>;
	const problems: string[] = [];
	if (k.kind !== 'kloom.kept-answer') problems.push('kind must be "kloom.kept-answer"');
	if (k.version !== 1) problems.push('version must be 1');
	if (typeof k.id !== 'string' || !ANSWER_ID.test(k.id)) problems.push('id is malformed');
	for (const f of ['subject', 'question', 'answer', 'provider', 'model', 'askedAt', 'keptAt'])
		if (!str(k[f])) problems.push(`${f} is required`);
	const anchor = k.anchor as Record<string, unknown> | undefined;
	if (!anchor || !str(anchor.frame)) problems.push('anchor.frame is required');
	else if (anchor.trail !== null && !str(anchor.trail))
		problems.push('anchor.trail must be a trail id or null');
	if (!Array.isArray(k.citations)) problems.push('citations must be an array');
	else
		k.citations.forEach((c, i) =>
			citationProblems(c).forEach((p) => problems.push(`citations[${i}]: ${p}`))
		);
	if (k.webCitations !== undefined) {
		if (!Array.isArray(k.webCitations)) problems.push('webCitations must be an array');
		else
			k.webCitations.forEach((c, i) =>
				citationProblems(c).forEach((p) => problems.push(`webCitations[${i}]: ${p}`))
			);
	}
	if (!Array.isArray(k.sources)) problems.push('sources must be an array');
	else
		k.sources.forEach((s, i) => {
			if (!s || !str((s as Source).title)) problems.push(`sources[${i}]: title is required`);
		});
	return problems;
}
