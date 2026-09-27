import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { appConfigProblems, loadAppConfig, resolveModel, type AppConfig } from './app-config';

const good: AppConfig = {
	provider: { kind: 'claude-cli', command: 'claude', timeoutSeconds: 120 },
	models: [
		{ id: 'claude-sonnet-5', label: 'Sonnet 5' },
		{ id: 'claude-opus-5-5', label: 'Opus 5.5' }
	],
	ask: { defaultModel: 'claude-sonnet-5' }
};

describe('the app config', () => {
	it('the committed kloom.config.json is valid, and defaults ask to Sonnet 5', async () => {
		const config = await loadAppConfig(
			join(import.meta.dirname, '..', '..', '..', 'kloom.config.json')
		);
		expect(config.ask.defaultModel).toBe('claude-sonnet-5');
		expect(config.models.find((m) => m.id === 'claude-sonnet-5')?.label).toBe('Sonnet 5');
	});

	it('finds every problem', () => {
		expect(appConfigProblems(good)).toEqual([]);
		expect(
			appConfigProblems({
				provider: { kind: 'claude-cli', command: '', timeoutSeconds: 0 },
				models: [
					{ id: '--dangerously-skip-permissions', label: 'x' },
					{ id: 'a', label: '' },
					{ id: 'a', label: 'A' }
				],
				ask: { defaultModel: 'b' }
			})
		).toEqual([
			'provider.command is required',
			'provider.timeoutSeconds must be a positive number',
			'models[0].id is not a model id',
			'models[1].label is required',
			'models[2].id repeats a',
			'ask.defaultModel must be one of the models'
		]);
		expect(appConfigProblems({ ...good, provider: { kind: 'other' } })).toContain(
			'provider.kind must be "claude-cli"'
		);
	});

	it('honours only a listed model id, falling back to the default', () => {
		expect(resolveModel(good, 'claude-opus-5-5')).toBe('claude-opus-5-5');
		expect(resolveModel(good, '--dangerously-skip-permissions')).toBe('claude-sonnet-5');
		expect(resolveModel(good, 'claude-opus-5-5 --tools default')).toBe('claude-sonnet-5');
		expect(resolveModel(good, undefined)).toBe('claude-sonnet-5');
		expect(resolveModel(good, { id: 'claude-opus-5-5' })).toBe('claude-sonnet-5');
	});
});
