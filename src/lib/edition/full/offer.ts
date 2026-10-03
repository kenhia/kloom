import { loadAppConfig, webMode } from '$lib/server/app-config';

/**
 * What the page offers the AI pane, from the app config (read per request,
 * so a model renamed there shows without a restart). The reader edition
 * offers none, and has no AI pane (korg 3500).
 */
export async function aiOffer() {
	const config = await loadAppConfig();
	const choices = config.models.map((m) => ({ value: m.id, label: m.label }));
	return {
		askModels: { choices, default: config.ask.defaultModel },
		askWeb: webMode(config),
		growModels: config.grow ? { choices, default: config.grow.defaultModel } : null
	};
}

export type AiOffered = Awaited<ReturnType<typeof aiOffer>> | null;
