import { join } from 'node:path';
import type { DatabaseSync } from 'node:sqlite';
import { env } from '$env/dynamic/private';
import type { ReaderStore } from '$engine/reader-data';
import { DEFAULT_DOMAIN, openAccounts, type Accounts } from './accounts';
import { openAskLedger, type AskLedger } from './ask-ledger';
import { dataDir } from './config';
import { openReaderDb, openReaderStore } from './sqlite-reader-store';

// The adapter lives in its own file so plain Node can load it (the review
// skill's script, the admin CLI); this one holds the app's shared instances.
export { openReaderStore, SCHEMA_VERSION, type SqliteReaderStore } from './sqlite-reader-store';

let db: DatabaseSync | null = null;
let shared: ReaderStore | null = null;
let accountsShared: Accounts | null = null;
let ledgerShared: AskLedger | null = null;

/** `<dataDir>/reader.db`, opened on first use; the store and the accounts share it. */
function readerDb(): DatabaseSync {
	db ??= openReaderDb(join(dataDir(), 'reader.db'));
	return db;
}

/** The app's store. */
export function readerStore(): ReaderStore {
	shared ??= openReaderStore(readerDb());
	return shared;
}

/**
 * The reader edition's accounts (korg 3501). Logins are `<username>@` the
 * domain, `$KLOOM_LOGIN_DOMAIN` or the reader site's own.
 */
export function accounts(): Accounts {
	accountsShared ??= openAccounts(readerDb(), {
		domain: env.KLOOM_LOGIN_DOMAIN || DEFAULT_DOMAIN
	});
	return accountsShared;
}

/** What API asks cost, and the reader site's allow-list (ask-ledger.ts), in the same file. */
export function askLedger(): AskLedger {
	ledgerShared ??= openAskLedger(readerDb());
	return ledgerShared;
}

/** Put another ledger in its place: tests use a throwaway one. */
export function useAskLedger(l: AskLedger) {
	ledgerShared = l;
}

/** Put another store in its place: tests use a throwaway one. */
export function useReaderStore(store: ReaderStore) {
	shared = store;
}

/** Put other accounts in their place: tests use throwaway ones. */
export function useAccounts(a: Accounts) {
	accountsShared = a;
}
