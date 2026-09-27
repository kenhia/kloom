import type { AskStreamEvent } from './provider';

/**
 * Read the ask endpoint's NDJSON body, calling `on` for each event in order.
 * Resolves when the body ends; a line that is not JSON is skipped.
 */
export async function readAskStream(
	body: ReadableStream<Uint8Array>,
	on: (event: AskStreamEvent) => void
): Promise<void> {
	const reader = body.getReader();
	const decoder = new TextDecoder();
	let buffer = '';
	const flush = (line: string) => {
		if (!line.trim()) return;
		let event: AskStreamEvent;
		try {
			event = JSON.parse(line);
		} catch {
			return; // Not ours; skip it.
		}
		on(event);
	};
	for (;;) {
		const { value, done } = await reader.read();
		if (done) break;
		buffer += decoder.decode(value, { stream: true });
		let nl: number;
		while ((nl = buffer.indexOf('\n')) >= 0) {
			flush(buffer.slice(0, nl));
			buffer = buffer.slice(nl + 1);
		}
	}
	flush(buffer + decoder.decode());
}
