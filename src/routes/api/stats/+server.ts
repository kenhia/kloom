import { json } from '@sveltejs/kit';
import { servedStats } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * The library's counts (docs/design.md §About), for the start screen's About
 * panel when it first opens. A read, open like the page.
 */
export const GET: RequestHandler = async () => json(await servedStats());
