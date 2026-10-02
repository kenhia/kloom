import type { Citation } from '../model';

/**
 * The provider interface (docs/design.md §AI). Every model call goes through
 * it, so a Claude API adapter, or another provider, is an additive change:
 * `claude -p` (./claude-cli.ts) is one adapter, not the architecture.
 */

/**
 * Whether ask may search the web (korg 3376), an app setting: `allow` offers
 * it checked, `offer` offers it unchecked, `deny` never adds the web tools.
 */
export const WEB_MODES = ['allow', 'offer', 'deny'] as const;
export type WebMode = (typeof WEB_MODES)[number];

/** What the app offers the AI pane, served by the page load from the app config. */
export interface AiOffer {
	web: WebMode;
	/** Whether grow is configured; the AI pane shows its form only then. */
	grow?: boolean;
}

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
		/** When a time-sensitive frame was last true (`YYYY-MM[-DD]`), if it says. */
		asOf?: string;
		/** Every citation, key sources and the rest (the Sources list derives from them). */
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
	/**
	 * Whether the model may search and read the web (WebSearch, WebFetch, and
	 * nothing else). The server has already checked it against the app config.
	 */
	web?: boolean;
	/** Aborting stops the turn (the reader pressed Stop, or went away). */
	signal?: AbortSignal;
}

/**
 * What a provider yields: the answer's text in order, or an error. A
 * `searching` status says the model went to the web; any text before it was
 * the model thinking aloud, not the answer, and is dropped.
 */
export type ProviderEvent =
	| { type: 'text'; text: string }
	| { type: 'status'; status: ProviderStatus }
	| { type: 'error'; message: string };

/** What the model is doing between words: an ask only ever searches. */
export type ProviderStatus = 'searching' | 'reading' | 'writing';

/**
 * One grow turn (docs/design.md §Grow): the model works on a copy of the
 * subject in `workDir`, with file tools confined to it. The host checks and
 * applies what it leaves there; the provider writes nothing else.
 */
export interface GrowRequest {
	/** An absolute path, outside the home directory, holding the subject's copy. */
	workDir: string;
	/** The content-writing instructions (skills/grow/SKILL.md), as the system prompt. */
	instructions: string;
	/** The job: verb, anchor, the reader's words. */
	prompt: string;
	model: string;
	/** WebSearch and WebFetch, for finding and pinning sources. */
	web: boolean;
	timeoutMs: number;
	signal?: AbortSignal;
	/**
	 * Told the process id of each model process the turn starts, so the host
	 * can record it (the grow queue's lock, docs/design.md §Grow). An adapter
	 * with no local process never calls it.
	 */
	onSpawn?: (pid: number) => void;
}

export interface Provider {
	/** Recorded on kept answers, e.g. "claude-cli". */
	readonly name: string;
	/**
	 * Stream one answer. The iterator ends when the answer is complete; a
	 * failure is an `error` event, after which it ends. Asking never writes
	 * subject content.
	 */
	ask(request: AskRequest): AsyncIterable<ProviderEvent>;
	/**
	 * Run one grow turn. Text is the model's account of what it did; a failure
	 * is an `error` event. The files are the result, not the events.
	 */
	grow(request: GrowRequest): AsyncIterable<ProviderEvent>;
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
