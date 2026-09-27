import { describe, expect, it } from 'vitest';
import { QueueFull, TurnQueue } from './queue';

describe('the turn queue', () => {
	it('runs one turn at a time, handing the slot on in order', async () => {
		const q = new TurnQueue(1, 3);
		const order: string[] = [];
		const release1 = await q.acquire();
		expect(q.busy).toBe(true);
		const second = q.acquire().then((r) => (order.push('second'), r));
		const third = q.acquire().then((r) => (order.push('third'), r));
		expect(q.waiting).toBe(2);
		release1();
		release1(); // releasing twice frees one slot, not two
		(await second)();
		(await third)();
		expect(order).toEqual(['second', 'third']);
		expect(q.busy).toBe(false);
	});

	it('refuses beyond the waiting limit', async () => {
		const q = new TurnQueue(1, 1);
		await q.acquire();
		void q.acquire();
		await expect(q.acquire()).rejects.toBeInstanceOf(QueueFull);
	});

	it('drops a waiter whose request is aborted', async () => {
		const q = new TurnQueue(1, 3);
		const release = await q.acquire();
		const abort = new AbortController();
		const waiting = q.acquire(abort.signal);
		abort.abort(new Error('gone'));
		await expect(waiting).rejects.toThrow('gone');
		expect(q.waiting).toBe(0);
		release();
		expect(q.busy).toBe(false);
	});
});
