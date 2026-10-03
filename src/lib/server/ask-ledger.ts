import type { DatabaseSync } from 'node:sqlite';
import type { AskUsage } from '$engine/ai/provider';
import type { AskCaps, Prices } from './app-config';

/**
 * What API asks cost, and who may ask on the reader site (docs/design.md
 * §Ask costs, §Ask on the reader site; korg 3529, 3530). It lives in
 * `reader.db` beside the accounts, in tables of its own (the store's
 * migration 6), and like the accounts it imports nothing but `node:`
 * modules and types, so the admin CLI loads it with plain Node.
 *
 * A row is one turn on a provider that bills by use: when, who, where, the
 * model, the tokens and searches the API reported, the time it took, and
 * its cost in US dollars from the configured price table. The question is
 * never kept here; a kept answer is the reader's, in the store.
 */

export interface AskCostRow {
	at: string;
	reader: string;
	subject: string;
	frame: string;
	provider: string;
	/** The model asked for. A fallback's own tokens are priced at its own rate, but logged here. */
	model: string;
	web: boolean;
	inputTokens: number;
	outputTokens: number;
	cacheReadTokens: number;
	cacheWriteTokens: number;
	webSearches: number;
	webFetches: number;
	ms: number;
	usd: number;
	/** `done`, `stopped` (the reader stopped it), `failed`, or `declined` (a refusal). */
	outcome: string;
}

export interface AskAccess {
	reader: string;
	/** Their own monthly cap; null means the configured default. */
	capUsd: number | null;
	enabled: string;
}

export interface RowFilter {
	/** ISO time or date, inclusive. */
	since?: string;
	/** ISO time or date, exclusive. */
	until?: string;
	reader?: string;
	model?: string;
}

export interface AskLedger {
	log(row: AskCostRow): void;
	rows(filter?: RowFilter): AskCostRow[];
	/** Dollars spent in `[since, until)`, by one reader or by everyone. */
	spent(since: string, until: string, reader?: string): number;
	/** The reader site's allow-list. */
	access(reader: string): AskAccess | null;
	allow(reader: string, capUsd: number | null, now?: Date): AskAccess;
	revoke(reader: string): boolean;
	allowed(): AskAccess[];
}

const COLUMNS = `at, reader, subject, frame, provider, model, web, input_tokens, output_tokens,
	cache_read_tokens, cache_write_tokens, web_searches, web_fetches, ms, usd, outcome`;

type Raw = Record<string, string | number | null>;

const fromRaw = (r: Raw): AskCostRow => ({
	at: r.at as string,
	reader: r.reader as string,
	subject: r.subject as string,
	frame: r.frame as string,
	provider: r.provider as string,
	model: r.model as string,
	web: r.web === 1,
	inputTokens: r.input_tokens as number,
	outputTokens: r.output_tokens as number,
	cacheReadTokens: r.cache_read_tokens as number,
	cacheWriteTokens: r.cache_write_tokens as number,
	webSearches: r.web_searches as number,
	webFetches: r.web_fetches as number,
	ms: r.ms as number,
	usd: r.usd as number,
	outcome: r.outcome as string
});

const accessOf = (r: Raw): AskAccess => ({
	reader: r.reader as string,
	capUsd: r.cap_usd as number | null,
	enabled: r.enabled as string
});

/** Open the ledger on a reader database already migrated (openReaderDb). */
export function openAskLedger(db: DatabaseSync): AskLedger {
	const insert = db.prepare(
		`INSERT INTO ask_cost (${COLUMNS}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
	);
	const spentAll = db.prepare(
		'SELECT coalesce(sum(usd), 0) AS usd FROM ask_cost WHERE at >= ? AND at < ?'
	);
	const spentBy = db.prepare(
		'SELECT coalesce(sum(usd), 0) AS usd FROM ask_cost WHERE at >= ? AND at < ? AND reader = ?'
	);
	const getAccess = db.prepare('SELECT reader, cap_usd, enabled FROM ask_access WHERE reader = ?');
	const putAccess = db.prepare(
		`INSERT INTO ask_access (reader, cap_usd, enabled) VALUES (?, ?, ?)
		 ON CONFLICT (reader) DO UPDATE SET cap_usd = excluded.cap_usd`
	);
	const dropAccess = db.prepare('DELETE FROM ask_access WHERE reader = ?');
	const allAccess = db.prepare('SELECT reader, cap_usd, enabled FROM ask_access ORDER BY reader');

	return {
		log(r) {
			insert.run(
				r.at,
				r.reader,
				r.subject,
				r.frame,
				r.provider,
				r.model,
				r.web ? 1 : 0,
				r.inputTokens,
				r.outputTokens,
				r.cacheReadTokens,
				r.cacheWriteTokens,
				r.webSearches,
				r.webFetches,
				Math.round(r.ms),
				r.usd,
				r.outcome
			);
		},
		rows(f = {}) {
			const where: string[] = [];
			const args: string[] = [];
			const add = (clause: string, value: string | undefined) => {
				if (!value) return;
				where.push(clause);
				args.push(value);
			};
			add('at >= ?', f.since);
			add('at < ?', f.until);
			add('reader = ?', f.reader);
			add('model = ?', f.model);
			const sql = `SELECT ${COLUMNS} FROM ask_cost ${where.length ? `WHERE ${where.join(' AND ')}` : ''} ORDER BY at, id`;
			return (db.prepare(sql).all(...args) as Raw[]).map(fromRaw);
		},
		spent(since, until, reader) {
			const row = (reader ? spentBy.get(since, until, reader) : spentAll.get(since, until)) as {
				usd: number;
			};
			return row.usd;
		},
		access(reader) {
			const r = getAccess.get(reader) as Raw | undefined;
			return r ? accessOf(r) : null;
		},
		allow(reader, capUsd, now = new Date()) {
			putAccess.run(reader, capUsd, now.toISOString());
			return accessOf(getAccess.get(reader) as Raw);
		},
		revoke(reader) {
			return dropAccess.run(reader).changes > 0;
		},
		allowed() {
			return (allAccess.all() as Raw[]).map(accessOf);
		}
	};
}

/**
 * A model id without its snapshot date: the API reports the model that
 * served a turn by its dated id (`claude-haiku-4-5-20251001`), and the price
 * table is keyed by the alias.
 */
export const undated = (model: string) => model.replace(/-\d{8}$/, '');

/**
 * What a turn cost, in US dollars: each model's tokens at its own price
 * (a model the table lacks at the dearest price it has, so a cap is never
 * undercounted), plus the searches.
 */
export function askCostUsd(usage: AskUsage, prices: Prices): number {
	const all = Object.values(prices.models);
	const dearest = all.reduce(
		(a, p) => ({
			input: Math.max(a.input, p.input),
			output: Math.max(a.output, p.output),
			cacheRead: Math.max(a.cacheRead, p.cacheRead),
			cacheWrite: Math.max(a.cacheWrite, p.cacheWrite)
		}),
		{ input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }
	);
	let usd = 0;
	for (const t of usage.tokens) {
		const p = prices.models[t.model] ?? prices.models[undated(t.model)] ?? dearest;
		usd +=
			(t.input * p.input +
				t.output * p.output +
				t.cacheRead * p.cacheRead +
				t.cacheWrite * p.cacheWrite) /
			1e6;
	}
	return usd + (usage.webSearches * prices.webSearchPerThousand) / 1000;
}

/** The ledger row's token columns for a usage: every model's tokens together. */
export function usageColumns(usage: AskUsage | null) {
	const sum = (k: 'input' | 'output' | 'cacheRead' | 'cacheWrite') =>
		(usage?.tokens ?? []).reduce((n, t) => n + t[k], 0);
	return {
		inputTokens: sum('input'),
		outputTokens: sum('output'),
		cacheReadTokens: sum('cacheRead'),
		cacheWriteTokens: sum('cacheWrite'),
		webSearches: usage?.webSearches ?? 0,
		webFetches: usage?.webFetches ?? 0
	};
}

// ---- Months and caps ----

/** The start of `now`'s calendar month and of the next, in UTC, as ISO times. */
export function monthOf(now: Date): { since: string; until: string; month: string } {
	const y = now.getUTCFullYear();
	const m = now.getUTCMonth();
	const since = new Date(Date.UTC(y, m, 1)).toISOString();
	const until = new Date(Date.UTC(y, m + 1, 1)).toISOString();
	return { since, until, month: since.slice(0, 7) };
}

/** A `YYYY-MM` month's bounds. */
export function monthBounds(month: string): { since: string; until: string; month: string } {
	const [y, m] = month.split('-').map(Number);
	return monthOf(new Date(Date.UTC(y, m - 1, 1)));
}

export const NEAR_SHARE = 0.8;

export interface Standing {
	month: string;
	reader: { spentUsd: number; capUsd: number };
	site: { spentUsd: number; capUsd: number };
	/** `resting` from the moment either cap is reached; `near` past `nearShare` of either. */
	state: 'open' | 'near' | 'resting';
	/** When ask comes back: the first of next month, `YYYY-MM-DD`. */
	until: string;
}

/** Where a reader stands against both caps this month. */
export function standing(
	ledger: AskLedger,
	reader: string,
	caps: AskCaps,
	now = new Date()
): Standing {
	const { since, until, month } = monthOf(now);
	const own = ledger.access(reader)?.capUsd ?? caps.readerUsd;
	const r = { spentUsd: ledger.spent(since, until, reader), capUsd: own };
	const s = { spentUsd: ledger.spent(since, until), capUsd: caps.siteUsd };
	const near = caps.nearShare ?? NEAR_SHARE;
	const state =
		r.spentUsd >= r.capUsd || s.spentUsd >= s.capUsd
			? 'resting'
			: r.spentUsd >= near * r.capUsd || s.spentUsd >= near * s.capUsd
				? 'near'
				: 'open';
	return { month, reader: r, site: s, state, until: until.slice(0, 10) };
}

// ---- Reports ----

const round = (usd: number, places = 4) => Number(usd.toFixed(places));

/** The nearest-rank percentile of sorted numbers. */
export function percentile(sorted: number[], p: number): number {
	if (!sorted.length) return 0;
	return sorted[Math.min(sorted.length - 1, Math.max(0, Math.ceil((p / 100) * sorted.length) - 1))];
}

export interface CostSummary {
	asks: number;
	totalUsd: number;
	meanUsd: number;
	p50Usd: number;
	p90Usd: number;
	maxUsd: number;
	/** Dollars per thousand output tokens. */
	usdPer1kOutput: number;
	/** Asks with web allowed, asks that searched, and the searching asks' share of the cost. */
	webAsks: number;
	searchedAsks: number;
	searchedCostShare: number;
	meanSeconds: number;
}

/** `just ask-costs`: the evidence a monthly cap is set from (korg 3529). */
export function summarize(rows: AskCostRow[]): CostSummary {
	const usd = rows.map((r) => r.usd).sort((a, b) => a - b);
	const total = usd.reduce((a, b) => a + b, 0);
	const output = rows.reduce((n, r) => n + r.outputTokens, 0);
	const searched = rows.filter((r) => r.webSearches > 0);
	const searchedUsd = searched.reduce((n, r) => n + r.usd, 0);
	return {
		asks: rows.length,
		totalUsd: round(total),
		meanUsd: round(rows.length ? total / rows.length : 0),
		p50Usd: round(percentile(usd, 50)),
		p90Usd: round(percentile(usd, 90)),
		maxUsd: round(usd.at(-1) ?? 0),
		usdPer1kOutput: round(output ? total / (output / 1000) : 0),
		webAsks: rows.filter((r) => r.web).length,
		searchedAsks: searched.length,
		searchedCostShare: round(total ? searchedUsd / total : 0, 3),
		meanSeconds: round(rows.length ? rows.reduce((n, r) => n + r.ms, 0) / rows.length / 1000 : 0, 1)
	};
}

/** The summary overall and per model, as text. */
export function costReport(rows: AskCostRow[]): string {
	const line = (label: string, s: CostSummary) =>
		`${label.padEnd(22)} ${String(s.asks).padStart(5)}  $${s.totalUsd.toFixed(4).padStart(9)}  ` +
		`$${s.meanUsd.toFixed(4)}  $${s.p50Usd.toFixed(4)}  $${s.p90Usd.toFixed(4)}  ` +
		`$${s.usdPer1kOutput.toFixed(4)}  ${String(s.searchedAsks).padStart(3)}/${String(s.webAsks).padEnd(3)}` +
		`  ${(s.searchedCostShare * 100).toFixed(0).padStart(3)}%  ${s.meanSeconds.toFixed(1)}s`;
	if (!rows.length) return 'no API asks logged';
	const models = [...new Set(rows.map((r) => r.model))].sort();
	return [
		`${'model'.padEnd(22)} ${'asks'.padStart(5)}  ${'total'.padStart(10)}  mean     p50      p90      per 1k out  searched/web  share  time`,
		...models.map((m) => line(m, summarize(rows.filter((r) => r.model === m)))),
		...(models.length > 1 ? [line('all', summarize(rows))] : [])
	].join('\n');
}

export interface UsageReport {
	month: string;
	generated: string;
	site: { spentUsd: number; capUsd: number | null; asks: number };
	readers: {
		reader: string;
		spentUsd: number;
		capUsd: number | null;
		asks: number;
		allowed: boolean;
	}[];
}

/**
 * The month's spend, site-wide and per reader, each with its cap: the
 * report kmon collects daily (korg 3530, 3533). Every allowed reader is
 * listed, asked or not, and anyone who spent.
 */
export function usageReport(
	ledger: AskLedger,
	caps: AskCaps | undefined,
	month: string,
	now = new Date()
): UsageReport {
	const { since, until } = monthBounds(month);
	const rows = ledger.rows({ since, until });
	const allowed = new Map(ledger.allowed().map((a) => [a.reader, a]));
	const who = [...new Set([...allowed.keys(), ...rows.map((r) => r.reader)])].sort();
	return {
		month,
		generated: now.toISOString(),
		site: {
			spentUsd: round(
				rows.reduce((n, r) => n + r.usd, 0),
				6
			),
			capUsd: caps?.siteUsd ?? null,
			asks: rows.length
		},
		readers: who.map((reader) => {
			const mine = rows.filter((r) => r.reader === reader);
			return {
				reader,
				spentUsd: round(
					mine.reduce((n, r) => n + r.usd, 0),
					6
				),
				capUsd: allowed.get(reader)?.capUsd ?? caps?.readerUsd ?? null,
				asks: mine.length,
				allowed: allowed.has(reader)
			};
		})
	};
}
