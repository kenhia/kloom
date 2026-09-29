import { join } from 'node:path';
import type { ReaderStore } from '$engine/reader-data';
import { dataDir } from './config';
import { openReaderStore } from './sqlite-reader-store';

// The adapter lives in its own file so plain Node can load it (the review
// skill's script); this one holds the app's shared instance.
export { openReaderStore, SCHEMA_VERSION, type SqliteReaderStore } from './sqlite-reader-store';

let shared: ReaderStore | null = null;

/** The app's store, opened on first use at `<dataDir>/reader.db`. */
export function readerStore(): ReaderStore {
	shared ??= openReaderStore(join(dataDir(), 'reader.db'));
	return shared;
}

/** Put another store in its place: tests use a throwaway one. */
export function useReaderStore(store: ReaderStore) {
	shared = store;
}
