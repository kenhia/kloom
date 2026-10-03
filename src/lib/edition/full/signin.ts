import { error, type Actions } from '@sveltejs/kit';
import type { load as readerLoad } from '../reader/signin';

/** The full edition has no accounts: kai's readers are its doors (reader.ts). */
export const load: typeof readerLoad = () => error(404, 'Not found');
export const actions: Actions = {};
