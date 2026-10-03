import { error, type Actions } from '@sveltejs/kit';
import type { load as readerLoad } from '../reader/welcome-link';

/** The full edition has no accounts, so no welcome links. */
export const load: typeof readerLoad = () => error(404, 'Not found');
export const actions: Actions = {};
