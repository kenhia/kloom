import type { BackStop } from '$engine/navigation';
import type { Reader } from '$lib/server/reader';

// See https://svelte.dev/docs/kit/types#app.d.ts
declare global {
	/** The build: its commit's short hash and date, stamped by vite.config.ts; empty outside git. */
	const __KLOOM_BUILD__: string;
	namespace App {
		interface Locals {
			/** Who is asking; null means the request may read but not write (korg 3388). */
			reader: Reader | null;
		}
		interface PageState {
			/** The jumps that led here, oldest first (§Connections); one per history entry. */
			back?: BackStop[];
		}
	}
}

export {};
