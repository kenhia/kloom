import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { env } from '$env/dynamic/private';

/**
 * App settings (docs/design.md §Settings): the deployment's, not a reader's.
 * They live in `kloom.config.json` (or `$KLOOM_CONFIG`) and are read per
 * request, so renaming a model is an edit to that file, not a code change.
 */

export interface ModelEntry {
	/** What `claude -p --model` gets. */
	id: string;
	/** What the reader sees in the settings drop-down. */
	label: string;
}

export interface AppConfig {
	provider: { kind: 'claude-cli'; command: string; timeoutSeconds: number };
	models: ModelEntry[];
	ask: { defaultModel: string };
}

/**
 * A model id: letters, digits, dots, dashes, underscores, and never a leading
 * dash, so even a hand-edited config cannot turn an id into a CLI flag.
 */
export const MODEL_ID = /^[A-Za-z0-9][\w.-]*$/;

export class AppConfigError extends Error {
	constructor(
		readonly path: string,
		readonly problems: string[]
	) {
		super(`app config ${path} is invalid:\n  ${problems.join('\n  ')}`);
		this.name = 'AppConfigError';
	}
}

/** Every problem with a parsed config; empty when it is usable. */
export function appConfigProblems(x: unknown): string[] {
	if (typeof x !== 'object' || x === null) return ['not an object'];
	const c = x as Record<string, unknown>;
	const problems: string[] = [];
	const provider = c.provider as Record<string, unknown> | undefined;
	if (provider?.kind !== 'claude-cli') problems.push('provider.kind must be "claude-cli"');
	else {
		if (typeof provider.command !== 'string' || !provider.command)
			problems.push('provider.command is required');
		if (typeof provider.timeoutSeconds !== 'number' || !(provider.timeoutSeconds > 0))
			problems.push('provider.timeoutSeconds must be a positive number');
	}
	const ids = new Set<string>();
	if (!Array.isArray(c.models) || c.models.length === 0) problems.push('models must be non-empty');
	else
		c.models.forEach((m: Record<string, unknown>, i) => {
			if (typeof m?.id !== 'string' || !MODEL_ID.test(m.id))
				problems.push(`models[${i}].id is not a model id`);
			else if (ids.has(m.id)) problems.push(`models[${i}].id repeats ${m.id}`);
			else ids.add(m.id);
			if (typeof m?.label !== 'string' || !m.label.trim())
				problems.push(`models[${i}].label is required`);
		});
	const ask = c.ask as Record<string, unknown> | undefined;
	if (typeof ask?.defaultModel !== 'string' || !ids.has(ask.defaultModel))
		problems.push('ask.defaultModel must be one of the models');
	return problems;
}

export const configPath = () => resolve(env.KLOOM_CONFIG ?? 'kloom.config.json');

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

/**
 * The model a request gets: the one it names if the config lists it,
 * otherwise the default. A client's string never reaches the command line.
 */
export function resolveModel(config: AppConfig, requested: unknown): string {
	return config.models.find((m) => m.id === requested)?.id ?? config.ask.defaultModel;
}
