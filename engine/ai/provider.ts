import type { Citation, Source } from '../model';

/**
 * The provider interface (docs/design.md §AI). Every model call goes through
 * it, so a Claude API adapter, or another provider, is an additive change:
 * `claude -p` (./claude-cli.ts) is one adapter, not the architecture.
 */

/** What the reader is looking at when they ask. The server builds it from disk. */
export interface AskContext {
	subject: { title: string };
	frame: {
		id: string;
		/** The reading pane's title: headline and accent word. */
		title: string;
		/** The HUD's position label, e.g. "AD 1440". */
		position: string;
		/** The segment the frame sits in, e.g. "The Renaissance". */
		segment: string;
		/** The reading as authored: markdown. */
		reading: string;
		sources: Source[];
		citations: Citation[];
	};
	/** Set while the reader is on a trail. */
	trail: { id: string; title: string } | null;
}

export interface AskRequest {
	context: AskContext;
	question: string;
	/** A model id the server has already checked against the app config. */
	model: string;
	/** Aborting stops the turn (the reader pressed Stop, or went away). */
	signal?: AbortSignal;
}

/** What a provider yields: the answer's text in order, or an error. */
export type ProviderEvent = { type: 'text'; text: string } | { type: 'error'; message: string };

export interface Provider {
	/** Recorded on kept answers, e.g. "claude-cli". */
	readonly name: string;
	/**
	 * Stream one answer. The iterator ends when the answer is complete; a
	 * failure is an `error` event, after which it ends. Asking never writes
	 * subject content.
	 */
	ask(request: AskRequest): AsyncIterable<ProviderEvent>;
}

/**
 * The ask endpoint's wire format: one JSON object per line. `start` names the
 * answer (the id "keep this" sends back); `queued` means another turn is
 * running and this one waits; exactly one `done` or `error` ends the stream.
 */
export type AskStreamEvent =
	| { type: 'start'; id: string; model: string; frame: string }
	| { type: 'queued' }
	| ProviderEvent
	| { type: 'done' };
