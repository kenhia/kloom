import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import {
	appConfigProblems,
	loadAppConfig,
	modelId,
	modelsOn,
	resolveModel,
	resolveWeb,
	type AppConfig
} from './app-config';

const prices = {
	checked: '2026-10-03',
	source: 'https://platform.claude.com/docs/en/about-claude/pricing',
	webSearchPerThousand: 10,
	models: { 'claude-haiku-4-5': { input: 1, output: 5, cacheRead: 0.1, cacheWrite: 1.25 } }
};

const good: AppConfig = {
	providers: [
		{ id: 'cli', kind: 'claude-cli', command: 'claude', timeoutSeconds: 120 },
		{ id: 'api', kind: 'anthropic-api', timeoutSeconds: 120 }
	],
	models: [
		{ id: 'claude-sonnet-5-5', label: 'Sonnet 5.5', provider: 'cli' },
		{ id: 'claude-opus-5-5', label: 'Opus 5.5', provider: 'cli' },
		{ id: 'api:claude-haiku-4-5', label: 'Haiku · API', provider: 'api', model: 'claude-haiku-4-5' }
	],
	prices,
	ask: { defaultModel: 'claude-sonnet-5-5' },
	grow: { defaultModel: 'claude-opus-5-5', timeoutSeconds: 900, web: true }
};

const root = join(import.meta.dirname, '..', '..', '..');

describe('the app config', () => {
	it('the committed kloom.config.json is valid, and defaults ask to Sonnet 5.5 on claude -p', async () => {
		const config = await loadAppConfig(join(root, 'kloom.config.json'));
		const ask = config.models.find((m) => m.id === config.ask.defaultModel)!;
		expect(ask.label).toBe('Sonnet 5.5');
		expect(modelId(ask)).toBe('claude-sonnet-5-5');
		expect(config.providers.find((p) => p.id === ask.provider)?.kind).toBe('claude-cli');
		expect(config.ask.web).toBe('allow');
		expect(config.grow?.defaultModel).toBe('claude-opus-5-5');
		// The API's models, side by side with claude -p's (korg 3529).
		expect(modelsOn(config, 'anthropic-api').map((m) => m.label)).toEqual([
			'Sonnet 5.5 · API',
			'Haiku 4.5 · API'
		]);
		expect(config.prices?.checked).toBe('2026-10-03');
		expect(config.ask.caps).toBeUndefined();
	});

	it('the reader edition’s kloom.reader.json: the API only, Haiku first, web on, $5 and $15 caps', async () => {
		const config = await loadAppConfig(join(root, 'kloom.reader.json'));
		expect(config.providers.map((p) => p.kind)).toEqual(['anthropic-api']);
		expect(config.models.map((m) => [m.label, modelId(m)])).toEqual([
			['Haiku 4.5', 'claude-haiku-4-5'],
			['Sonnet 5.5', 'claude-sonnet-5-5']
		]);
		expect(config.ask.defaultModel).toBe('api:claude-haiku-4-5');
		expect(config.models.find((m) => modelId(m) === 'claude-sonnet-5-5')?.fallbacks).toBe(true);
		expect(config.ask.web).toBe('allow');
		expect(config.ask.caps).toEqual({ readerUsd: 5, siteUsd: 15, nearShare: 0.8 });
		expect(config.grow).toBeUndefined();
		const api = config.providers[0];
		expect(api.kind === 'anthropic-api' && api.web).toEqual({
			searchMaxUses: 3,
			fetchMaxUses: 2,
			fetchMaxContentTokens: 8000
		});
	});

	it('finds every problem', () => {
		expect(appConfigProblems(good)).toEqual([]);
		expect(
			appConfigProblems({
				providers: [{ id: 'cli', kind: 'claude-cli', command: '', timeoutSeconds: 0 }],
				models: [
					{ id: '--dangerously-skip-permissions', label: 'x', provider: 'cli' },
					{ id: 'a', label: '', provider: 'cli' },
					{ id: 'a', label: 'A', provider: 'nope' }
				],
				ask: { defaultModel: 'b' }
			})
		).toEqual([
			'providers[0].timeoutSeconds must be a positive number',
			'providers[0].command is required',
			'models[0].id is not an id',
			'models[0].id is not a model id',
			'models[1].label is required',
			'models[2].id repeats a',
			'models[2].provider must be one of the providers',
			'ask.defaultModel must be one of the models'
		]);
		expect(
			appConfigProblems({
				...good,
				providers: [
					{ ...good.providers[0], webTimeoutSeconds: -1 },
					{ id: 'api', kind: 'anthropic-api', timeoutSeconds: 60, web: { searchMaxUses: 0 } }
				],
				ask: { defaultModel: 'claude-sonnet-5-5', web: 'always', caps: { readerUsd: 0 } },
				grow: { defaultModel: 'gpt', timeoutSeconds: '900', web: 'yes' }
			})
		).toEqual([
			'providers[0].webTimeoutSeconds must be a positive number',
			'providers[1].web.searchMaxUses must be a positive whole number',
			'ask.web must be one of allow, offer, deny',
			'ask.caps.readerUsd must be a positive number',
			'ask.caps.siteUsd must be a positive number',
			'grow.defaultModel must be one of the models',
			'grow.timeoutSeconds must be a positive number',
			'grow.web must be true or false'
		]);
		expect(
			appConfigProblems({ ...good, providers: [{ id: 'x', kind: 'other' }], models: [] })
		).toContain('providers[0].kind must be one of claude-cli, anthropic-api');
	});

	it('wants a price for every model on the API, and keeps grow on claude -p', () => {
		expect(appConfigProblems({ ...good, prices: undefined })).toEqual([
			'models[2] is on the API, so prices.models needs claude-haiku-4-5'
		]);
		expect(
			appConfigProblems({ ...good, grow: { ...good.grow!, defaultModel: 'api:claude-haiku-4-5' } })
		).toEqual(['grow.defaultModel must be on a claude-cli provider']);
		expect(
			appConfigProblems({
				...good,
				models: [{ ...good.models[0], fallbacks: true }, ...good.models.slice(1)]
			})
		).toEqual(["models[0].fallbacks is the API's; claude -p has none"]);
		expect(appConfigProblems({ ...good, prices: { ...prices, checked: 'today' } })).toEqual([
			'prices.checked must be the date they were checked (YYYY-MM-DD)'
		]);
	});

	it('honours only a listed model, falling back to the default', () => {
		const id = (x: unknown, fallback?: string) => resolveModel(good, x, fallback).id;
		expect(id('claude-opus-5-5')).toBe('claude-opus-5-5');
		expect(id('api:claude-haiku-4-5')).toBe('api:claude-haiku-4-5');
		expect(id('--dangerously-skip-permissions')).toBe('claude-sonnet-5-5');
		expect(id('claude-opus-5-5 --tools default')).toBe('claude-sonnet-5-5');
		expect(id(undefined)).toBe('claude-sonnet-5-5');
		expect(id({ id: 'claude-opus-5-5' })).toBe('claude-sonnet-5-5');
		expect(id('nope', 'claude-opus-5-5')).toBe('claude-opus-5-5');
		// Grow chooses among claude -p's models only.
		const cli = modelsOn(good, 'claude-cli');
		expect(resolveModel(good, 'api:claude-haiku-4-5', 'claude-opus-5-5', cli).id).toBe(
			'claude-opus-5-5'
		);
	});

	it('uses the web only when the reader asks and the config allows or offers it', () => {
		const ask = (web?: 'allow' | 'offer' | 'deny') => ({ ...good, ask: { ...good.ask, web } });
		expect(resolveWeb(ask('allow'), true)).toBe(true);
		expect(resolveWeb(ask('offer'), true)).toBe(true);
		expect(resolveWeb(ask('allow'), false)).toBe(false);
		expect(resolveWeb(ask('deny'), true)).toBe(false);
		expect(resolveWeb(ask(), true)).toBe(false);
		expect(resolveWeb(ask('allow'), 'true')).toBe(false);
	});
});
