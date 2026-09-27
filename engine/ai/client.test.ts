import { describe, expect, it } from 'vitest';
import { readAskStream } from './client';
import type { AskStreamEvent } from './provider';

const body = (...chunks: string[]) =>
	new ReadableStream<Uint8Array>({
		start(c) {
			for (const s of chunks) c.enqueue(new TextEncoder().encode(s));
			c.close();
		}
	});

describe('reading the ask stream', () => {
	it('yields each event in order, across chunk boundaries, skipping junk', async () => {
		const got: AskStreamEvent[] = [];
		await readAskStream(
			body(
				'{"type":"start","id":"a","model":"m","frame":"f"}\n{"type":"te',
				'xt","text":"Hi"}\nnoise\n',
				'{"type":"done"}'
			),
			(e) => got.push(e)
		);
		expect(got.map((e) => e.type)).toEqual(['start', 'text', 'done']);
	});
});
