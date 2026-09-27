/**
 * Model turns run one at a time on the host; a few more may wait their turn,
 * and beyond that a request is refused rather than piling up.
 */

export class QueueFull extends Error {
	constructor() {
		super('Too many questions are waiting; try again in a moment.');
		this.name = 'QueueFull';
	}
}

export class TurnQueue {
	#running = 0;
	#waiting: Array<{ go: () => void }> = [];

	constructor(
		readonly concurrency = 1,
		readonly maxWaiting = 3
	) {}

	/** Whether a turn asked for now would have to wait. */
	get busy() {
		return this.#running >= this.concurrency;
	}

	get waiting() {
		return this.#waiting.length;
	}

	/**
	 * Wait for a slot; resolves with the function that frees it. Rejects with
	 * `QueueFull`, or with the signal's reason if it aborts while waiting.
	 */
	acquire(signal?: AbortSignal): Promise<() => void> {
		if (signal?.aborted) return Promise.reject(signal.reason);
		if (!this.busy) {
			this.#running++;
			return Promise.resolve(this.#release());
		}
		if (this.#waiting.length >= this.maxWaiting) return Promise.reject(new QueueFull());
		return new Promise((resolve, reject) => {
			const entry = {
				go: () => {
					signal?.removeEventListener('abort', onAbort);
					this.#running++;
					resolve(this.#release());
				}
			};
			const onAbort = () => {
				this.#waiting = this.#waiting.filter((w) => w !== entry);
				reject(signal!.reason);
			};
			signal?.addEventListener('abort', onAbort, { once: true });
			this.#waiting.push(entry);
		});
	}

	#release() {
		let done = false;
		return () => {
			if (done) return;
			done = true;
			this.#running--;
			this.#waiting.shift()?.go();
		};
	}
}
