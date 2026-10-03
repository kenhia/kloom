/**
 * Backoff for sign-in (korg 3501): failures are counted per key (a username,
 * a client address), and past a free allowance each one locks that key out
 * for twice as long as the last, up to a ceiling. A success clears the key.
 * Held in memory: the reader site is one process on one machine, and a
 * restart forgiving everyone is acceptable.
 */
export interface LimitPolicy {
	/** Failures before the first lockout: the next try after that many waits. */
	free: number;
	/** The first lockout, in ms; each failure after doubles it. */
	base: number;
	/** The longest lockout, in ms. */
	max: number;
	/** A key with no failure for this long is forgotten, in ms. */
	forget: number;
}

interface Entry {
	failures: number;
	until: number;
	last: number;
}

export class RateLimit {
	readonly #entries = new Map<string, Entry>();

	constructor(
		readonly policy: LimitPolicy,
		private readonly now: () => number = Date.now
	) {}

	/** How many ms until any of `keys` may try again; 0 when all may now. */
	wait(keys: string[]): number {
		const at = this.now();
		let wait = 0;
		for (const k of keys) {
			const e = this.#fresh(k, at);
			if (e && e.until > at) wait = Math.max(wait, e.until - at);
		}
		return wait;
	}

	/** A failed attempt under each key. */
	fail(keys: string[]) {
		const at = this.now();
		const { free, base, max } = this.policy;
		for (const k of keys) {
			const e = this.#fresh(k, at) ?? { failures: 0, until: 0, last: at };
			e.failures++;
			e.last = at;
			if (e.failures >= free) e.until = at + Math.min(max, base * 2 ** (e.failures - free));
			this.#entries.set(k, e);
		}
		this.#prune(at);
	}

	/** A success: these keys start afresh. */
	succeed(keys: string[]) {
		for (const k of keys) this.#entries.delete(k);
	}

	#fresh(key: string, at: number): Entry | null {
		const e = this.#entries.get(key);
		if (!e) return null;
		if (at - e.last > this.policy.forget && e.until <= at) {
			this.#entries.delete(key);
			return null;
		}
		return e;
	}

	/** Keep the map from growing without end under a spray of usernames. */
	#prune(at: number) {
		if (this.#entries.size < 10_000) return;
		for (const [k] of this.#entries) this.#fresh(k, at);
	}
}

/** Sign-in's own: five tries free per username, twenty per address, then 30 s doubling to 15 minutes. */
export const signInLimits = {
	user: { free: 5, base: 30_000, max: 15 * 60_000, forget: 60 * 60_000 },
	address: { free: 20, base: 30_000, max: 15 * 60_000, forget: 60 * 60_000 }
} satisfies Record<string, LimitPolicy>;
