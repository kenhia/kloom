import { resolve } from 'node:path';
import { env } from '$env/dynamic/private';

/**
 * Which subject this app serves. The engine never names one; this is the
 * app's choice, overridable per deployment.
 */
export const subjectDir = () =>
	resolve(env.KLOOM_SUBJECTS_DIR ?? 'subjects', env.KLOOM_SUBJECT ?? 'western-civ');

/**
 * Where the app keeps what it writes that is not subject content, such as
 * kept answers (`<dataDir>/<subject>/kept/`). Git-ignored.
 */
export const dataDir = () => resolve(env.KLOOM_DATA_DIR ?? 'data');
