import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { env } from '$env/dynamic/private';
import { WEB_MODES, type WebMode } from '$engine/ai/provider';

/**
 * App settings (docs/design.md §Settings): the deployment's, not a reader's.
 * They live in `kloom.config.json` (or `$KLOOM_CONFIG`) and are read per
 * request, so renaming a model is an edit to that file, not a code change.
 */

/** `claude -p` on the host, under its logged-in subscription. */
export interface CliProviderConfig {
	id: string;
	kind: 'claude-cli';
	command: string;
	timeoutSeconds: number;
	/** A web turn searches and reads pages first; 180 when absent. */
	webTimeoutSeconds?: number;
}

/** The Claude API with an API key (korg 3529): ask only, priced and logged. */
export interface ApiProviderConfig {
	id: string;
	kind: 'anthropic-api';
	timeoutSeconds: number;
	webTimeoutSeconds?: number;
	/** The environment variable holding the key; `ANTHROPIC_API_KEY` when absent. */
	keyEnv?: string;
	/**
	 * A dotenv file the key is read from when the environment lacks it: kai's
	 * `/etc/khomelab/secrets.env`, from which only that one key is taken.
	 */
	keyFile?: string;
	/** The web's caps on one turn; each absent one is the measured default (3, 2, 8000). */
	web?: { searchMaxUses?: number; fetchMaxUses?: number; fetchMaxContentTokens?: number };
}

export type ProviderConfig = CliProviderConfig | ApiProviderConfig;

export interface ModelEntry {
	/** What the reader's setting stores: unique in the list. */
	id: string;
	/** What the reader sees in the settings drop-down. */
	label: string;
	/** The id of the provider that runs it. */
	provider: string;
	/** The model id the provider is given (`claude -p --model`, the API's `model`); `id` when absent. */
	model?: string;
	/** API only: send the server-side refusal fallback (`fallbacks: "default"`). */
	fallbacks?: boolean;
}

/** A model's price in US dollars per million tokens. */
export interface Price {
	input: number;
	output: number;
	cacheRead: number;
	cacheWrite: number;
}

/**
 * What API asks cost (docs/design.md §Ask costs). Checked by hand against
 * Anthropic's pricing page, never taken from memory: `checked` says when.
 */
export interface Prices {
	checked: string;
	source: string;
	/** Web search is billed per search, on top of the tokens it reads. */
	webSearchPerThousand: number;
	models: Record<string, Price>;
}

/** Monthly caps on API asks, in US dollars (docs/design.md §Ask on the reader site). */
export interface AskCaps {
	/** Each reader's, unless the admin CLI set them their own. */
	readerUsd: number;
	/** Everyone's together: the backstop before the Console's own limit. */
	siteUsd: number;
	/** The share of a cap past which the reader is told they are near it; 0.8 when absent. */
	nearShare?: number;
}

export interface AppConfig {
	providers: ProviderConfig[];
	models: ModelEntry[];
	/** Required once any model is on the API. */
	prices?: Prices;
	/** `web` absent means `deny`; `caps` absent means uncapped. */
	ask: { defaultModel: string; web?: WebMode; caps?: AskCaps };
	/** Absent: grow is not offered. Its models must be on `claude -p`. */
	grow?: {
		defaultModel: string;
		/** A job that runs longer is killed and fails. */
		timeoutSeconds: number;
		/** Whether a grow job may search and read the web for its sources. */
		web: boolean;
	};
}

/**
 * A model id: letters, digits, dots, dashes, underscores, and never a leading
 * dash, so even a hand-edited config cannot turn an id into a CLI flag.
 */
export const MODEL_ID = /^[A-Za-z0-9][\w.-]*$/;
/** An entry's or a provider's id: a model id that may also hold a colon (`api:…`). */
export const ENTRY_ID = /^[A-Za-z0-9][\w.:-]*$/;

export const PROVIDER_KINDS = ['claude-cli', 'anthropic-api'] as const;

export class AppConfigError extends Error {
	constructor(
		readonly path: string,
		readonly problems: string[]
	) {
		super(`app config ${path} is invalid:\n  ${problems.join('\n  ')}`);
		this.name = 'AppConfigError';
	}
}

const positive = (x: unknown) => typeof x === 'number' && x > 0;
const nonNegative = (x: unknown) => typeof x === 'number' && x >= 0;

/** The model id a provider is given for an entry. */
export const modelId = (m: ModelEntry) => m.model ?? m.id;

/** Every problem with a parsed config; empty when it is usable. */
export function appConfigProblems(x: unknown): string[] {
	if (typeof x !== 'object' || x === null) return ['not an object'];
	const c = x as Record<string, unknown>;
	const problems: string[] = [];

	const kinds = new Map<string, string>();
	if (!Array.isArray(c.providers) || c.providers.length === 0)
		problems.push('providers must be non-empty');
	else
		c.providers.forEach((p: Record<string, unknown>, i) => {
			const at = `providers[${i}]`;
			if (typeof p?.id !== 'string' || !ENTRY_ID.test(p.id)) problems.push(`${at}.id is not an id`);
			else if (kinds.has(p.id)) problems.push(`${at}.id repeats ${p.id}`);
			if (!PROVIDER_KINDS.includes(p?.kind as never)) {
				problems.push(`${at}.kind must be one of ${PROVIDER_KINDS.join(', ')}`);
				return;
			}
			if (typeof p.id === 'string') kinds.set(p.id, p.kind as string);
			if (!positive(p.timeoutSeconds))
				problems.push(`${at}.timeoutSeconds must be a positive number`);
			if (p.webTimeoutSeconds !== undefined && !positive(p.webTimeoutSeconds))
				problems.push(`${at}.webTimeoutSeconds must be a positive number`);
			if (p.kind === 'claude-cli' && (typeof p.command !== 'string' || !p.command))
				problems.push(`${at}.command is required`);
			if (p.kind === 'anthropic-api') {
				for (const k of ['keyEnv', 'keyFile'])
					if (p[k] !== undefined && (typeof p[k] !== 'string' || !p[k]))
						problems.push(`${at}.${k} must be a non-empty string`);
				const web = p.web as Record<string, unknown> | undefined;
				if (web !== undefined)
					for (const k of ['searchMaxUses', 'fetchMaxUses', 'fetchMaxContentTokens'])
						if (web?.[k] !== undefined && !(Number.isInteger(web[k]) && positive(web[k])))
							problems.push(`${at}.web.${k} must be a positive whole number`);
			}
		});

	const prices = c.prices as Record<string, unknown> | undefined;
	const priced = (prices?.models ?? {}) as Record<string, Record<string, unknown>>;
	if (prices !== undefined) {
		if (typeof prices?.checked !== 'string' || !/^\d{4}-\d\d-\d\d$/.test(prices.checked))
			problems.push('prices.checked must be the date they were checked (YYYY-MM-DD)');
		if (typeof prices?.source !== 'string' || !prices.source)
			problems.push('prices.source must say where they were checked');
		if (!nonNegative(prices?.webSearchPerThousand))
			problems.push('prices.webSearchPerThousand must be a number');
		for (const [id, p] of Object.entries(priced))
			for (const k of ['input', 'output', 'cacheRead', 'cacheWrite'])
				if (!nonNegative(p?.[k])) problems.push(`prices.models.${id}.${k} must be a number`);
	}

	const entries = new Map<string, string>();
	if (!Array.isArray(c.models) || c.models.length === 0) problems.push('models must be non-empty');
	else
		c.models.forEach((m: Record<string, unknown>, i) => {
			const at = `models[${i}]`;
			if (typeof m?.id !== 'string' || !ENTRY_ID.test(m.id)) problems.push(`${at}.id is not an id`);
			else if (entries.has(m.id)) problems.push(`${at}.id repeats ${m.id}`);
			const model = m?.model ?? m?.id;
			if (typeof model !== 'string' || !MODEL_ID.test(model))
				problems.push(`${at}.${m?.model === undefined ? 'id' : 'model'} is not a model id`);
			if (typeof m?.label !== 'string' || !m.label.trim()) problems.push(`${at}.label is required`);
			const kind = kinds.get(m?.provider as string);
			if (!kind) problems.push(`${at}.provider must be one of the providers`);
			if (m?.fallbacks !== undefined && typeof m.fallbacks !== 'boolean')
				problems.push(`${at}.fallbacks must be true or false`);
			if (kind === 'anthropic-api' && typeof model === 'string' && !priced[model])
				problems.push(`${at} is on the API, so prices.models needs ${model}`);
			if (m?.fallbacks && kind !== 'anthropic-api')
				problems.push(`${at}.fallbacks is the API's; claude -p has none`);
			if (typeof m?.id === 'string') entries.set(m.id, kind ?? '');
		});

	const ask = c.ask as Record<string, unknown> | undefined;
	if (typeof ask?.defaultModel !== 'string' || !entries.has(ask.defaultModel))
		problems.push('ask.defaultModel must be one of the models');
	if (ask?.web !== undefined && !WEB_MODES.includes(ask.web as WebMode))
		problems.push(`ask.web must be one of ${WEB_MODES.join(', ')}`);
	const caps = ask?.caps as Record<string, unknown> | undefined;
	if (caps !== undefined) {
		if (!positive(caps?.readerUsd)) problems.push('ask.caps.readerUsd must be a positive number');
		if (!positive(caps?.siteUsd)) problems.push('ask.caps.siteUsd must be a positive number');
		if (
			caps?.nearShare !== undefined &&
			!(typeof caps.nearShare === 'number' && caps.nearShare > 0 && caps.nearShare < 1)
		)
			problems.push('ask.caps.nearShare must be between 0 and 1');
	}

	const grow = c.grow as Record<string, unknown> | undefined;
	if (grow !== undefined) {
		if (typeof grow?.defaultModel !== 'string' || !entries.has(grow.defaultModel))
			problems.push('grow.defaultModel must be one of the models');
		else if (entries.get(grow.defaultModel) !== 'claude-cli')
			problems.push('grow.defaultModel must be on a claude-cli provider');
		if (!positive(grow?.timeoutSeconds))
			problems.push('grow.timeoutSeconds must be a positive number');
		if (typeof grow?.web !== 'boolean') problems.push('grow.web must be true or false');
	}
	return problems;
}

let pathOverride: string | null = null;

export const configPath = () => resolve(pathOverride ?? env.KLOOM_CONFIG ?? 'kloom.config.json');

/** Read another config file in its place (tests: the reader edition's); null puts it back. */
export function useConfigPath(path: string | null) {
	pathOverride = path;
}

export async function loadAppConfig(path = configPath()): Promise<AppConfig> {
	let raw: unknown;
	try {
		raw = JSON.parse(await readFile(path, 'utf8'));
	} catch (e) {
		throw new AppConfigError(path, [(e as Error).message]);
	}
	const problems = appConfigProblems(raw);
	if (problems.length) throw new AppConfigError(path, problems);
	return raw as AppConfig;
}

/** A provider by id; the config was validated, so a model's provider exists. */
export const providerConfig = (config: AppConfig, id: string): ProviderConfig =>
	config.providers.find((p) => p.id === id)!;

/** The models one kind of provider runs. */
export const modelsOn = (config: AppConfig, kind: ProviderConfig['kind']): ModelEntry[] =>
	config.models.filter((m) => providerConfig(config, m.provider).kind === kind);

/**
 * The model a request gets: the entry it names if the config lists it among
 * `among` (every model by default), otherwise the default. A client's string
 * never reaches a command line or the API.
 */
export function resolveModel(
	config: AppConfig,
	requested: unknown,
	fallback = config.ask.defaultModel,
	among: ModelEntry[] = config.models
): ModelEntry {
	return among.find((m) => m.id === requested) ?? config.models.find((m) => m.id === fallback)!;
}

/** How ask offers the web; absent in the config means `deny`. */
export const webMode = (config: AppConfig): WebMode => config.ask.web ?? 'deny';

/**
 * Whether a turn searches the web: only when the reader asked for it and the
 * config does not deny it. A request can never turn the web on past `deny`.
 */
export const resolveWeb = (config: AppConfig, requested: unknown): boolean =>
	requested === true && webMode(config) !== 'deny';
