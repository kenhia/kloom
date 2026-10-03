import { describe, expect, it } from 'vitest';
import {
	askCostUsd,
	costReport,
	monthOf,
	openAskLedger,
	percentile,
	standing,
	summarize,
	usageReport,
	type AskCostRow
} from './ask-ledger';
import { openReaderDb } from './sqlite-reader-store';

const prices = {
	checked: '2026-10-03',
	source: 'test',
	webSearchPerThousand: 10,
	models: {
		'claude-haiku-4-5': { input: 1, output: 5, cacheRead: 0.1, cacheWrite: 1.25 },
		'claude-sonnet-5-5': { input: 2, output: 10, cacheRead: 0.2, cacheWrite: 2.5 }
	}
};

const row = (o: Partial<AskCostRow>): AskCostRow => ({
	at: '2026-10-03T12:00:00.000Z',
	reader: 'jkh@kloom.example',
	subject: 'blood',
	frame: 'harvey',
	provider: 'anthropic-api',
	model: 'claude-haiku-4-5',
	web: false,
	inputTokens: 3000,
	outputTokens: 400,
	cacheReadTokens: 0,
	cacheWriteTokens: 0,
	webSearches: 0,
	webFetches: 0,
	ms: 2000,
	usd: 0.005,
	outcome: 'done',
	...o
});

describe('pricing a turn', () => {
	it('prices each model’s tokens at its own rate, and every search', () => {
		const usd = askCostUsd(
			{
				tokens: [
					{ model: 'claude-haiku-4-5', input: 1e6, output: 1e5, cacheRead: 1e6, cacheWrite: 1e5 },
					{ model: 'claude-sonnet-5-5', input: 1e5, output: 1e4, cacheRead: 0, cacheWrite: 0 }
				],
				webSearches: 3,
				webFetches: 2
			},
			prices
		);
		// Haiku 1 + 0.5 + 0.1 + 0.125; Sonnet 0.2 + 0.1; searches 0.03.
		expect(usd).toBeCloseTo(2.055, 10);
	});

	it('prices a dated model id, as the API reports the model that served, at its alias’s rate', () => {
		expect(
			askCostUsd(
				{
					tokens: [
						{
							model: 'claude-haiku-4-5-20251001',
							input: 2690,
							output: 50,
							cacheRead: 0,
							cacheWrite: 0
						}
					],
					webSearches: 0,
					webFetches: 0
				},
				prices
			)
		).toBeCloseTo(0.00294, 10);
	});

	it('prices a model the table lacks at the dearest rate it has, so a cap never undercounts', () => {
		expect(
			askCostUsd(
				{
					tokens: [{ model: 'claude-new', input: 1e6, output: 0, cacheRead: 0, cacheWrite: 0 }],
					webSearches: 0,
					webFetches: 0
				},
				prices
			)
		).toBe(2);
	});
});

describe('months and caps', () => {
	it('counts calendar months in UTC, and rests until the first of the next', () => {
		expect(monthOf(new Date('2026-12-31T23:59:59Z'))).toEqual({
			since: '2026-12-01T00:00:00.000Z',
			until: '2027-01-01T00:00:00.000Z',
			month: '2026-12'
		});
	});

	it('stands open, near past 80% of either cap, and resting at either, with a reader’s own cap', () => {
		const ledger = openAskLedger(openReaderDb(':memory:'));
		const now = new Date('2026-10-20T00:00:00Z');
		const caps = { readerUsd: 5, siteUsd: 15 };
		const at = (r: string) => standing(ledger, r, caps, now);
		expect(at('jkh')).toMatchObject({ state: 'open', until: '2026-11-01', month: '2026-10' });
		ledger.log(row({ reader: 'jkh', usd: 3.9 }));
		ledger.log(row({ reader: 'jkh', usd: 9, at: '2026-09-30T23:59:59.999Z' }));
		expect(at('jkh').state).toBe('open');
		ledger.log(row({ reader: 'jkh', usd: 0.2 }));
		expect(at('jkh')).toMatchObject({ state: 'near', reader: { spentUsd: 4.1, capUsd: 5 } });
		ledger.allow('jkh', 4);
		expect(at('jkh').state).toBe('resting');
		expect(at('other').state).toBe('open');
		ledger.log(row({ reader: 'other', usd: 11 }));
		expect(at('other')).toMatchObject({ state: 'resting', site: { capUsd: 15 } });
	});
});

describe('the allow-list', () => {
	it('allows, changes a cap, and revokes', () => {
		const ledger = openAskLedger(openReaderDb(':memory:'));
		const t = new Date('2026-10-03T00:00:00Z');
		expect(ledger.access('jkh')).toBeNull();
		expect(ledger.allow('jkh', null, t)).toEqual({
			reader: 'jkh',
			capUsd: null,
			enabled: t.toISOString()
		});
		expect(ledger.allow('jkh', 7).enabled).toBe(t.toISOString());
		expect(ledger.access('jkh')?.capUsd).toBe(7);
		expect(ledger.allowed().map((a) => a.reader)).toEqual(['jkh']);
		expect(ledger.revoke('jkh')).toBe(true);
		expect(ledger.revoke('jkh')).toBe(false);
	});
});

describe('reports', () => {
	it('summarizes cost per ask: mean, p50, p90, per 1k output, and the web’s share', () => {
		const rows = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) =>
			row({ usd: n / 100, outputTokens: 1000, web: n > 5, webSearches: n > 8 ? 1 : 0 })
		);
		expect(summarize(rows)).toEqual({
			asks: 10,
			totalUsd: 0.55,
			meanUsd: 0.055,
			p50Usd: 0.05,
			p90Usd: 0.09,
			maxUsd: 0.1,
			usdPer1kOutput: 0.055,
			webAsks: 5,
			searchedAsks: 2,
			searchedCostShare: 0.345,
			meanSeconds: 2
		});
		expect(percentile([], 50)).toBe(0);
		expect(costReport(rows)).toContain('claude-haiku-4-5');
		expect(costReport([])).toBe('no API asks logged');
	});

	it('reports the month for kmon: site and every reader, each with a cap, matching the rows', () => {
		const ledger = openAskLedger(openReaderDb(':memory:'));
		ledger.allow('jkh', null);
		ledger.allow('quiet', 2);
		ledger.log(row({ reader: 'jkh', usd: 0.01 }));
		ledger.log(row({ reader: 'jkh', usd: 0.02 }));
		ledger.log(row({ reader: 'gone', usd: 0.5 }));
		ledger.log(row({ reader: 'jkh', usd: 9, at: '2026-11-01T00:00:00.000Z' }));
		const r = usageReport(
			ledger,
			{ readerUsd: 5, siteUsd: 15 },
			'2026-10',
			new Date('2026-10-04T00:00:00Z')
		);
		expect(r).toEqual({
			month: '2026-10',
			generated: '2026-10-04T00:00:00.000Z',
			site: { spentUsd: 0.53, capUsd: 15, asks: 3 },
			readers: [
				{ reader: 'gone', spentUsd: 0.5, capUsd: 5, asks: 1, allowed: false },
				{ reader: 'jkh', spentUsd: 0.03, capUsd: 5, asks: 2, allowed: true },
				{ reader: 'quiet', spentUsd: 0, capUsd: 2, asks: 0, allowed: true }
			]
		});
	});
});
