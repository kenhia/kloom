import { loadAppConfig, modelsOn, webMode, type AppConfig } from './app-config';
import { standing } from './ask-ledger';
import { askLedger } from './reader-store';

/**
 * What the page offers the AI pane, from the app config (read per request,
 * so a model renamed there shows without a restart). Grow's choices are the
 * models on `claude -p`; with caps in the config, the reader's standing
 * comes too, so the pane can say ask is resting before they type.
 */
export async function offerFor(reader: string | null, config?: AppConfig) {
	config ??= await loadAppConfig();
	const caps = config.ask.caps;
	const budget =
		caps && reader
			? (({ state, until }) => ({ state, until }))(standing(askLedger(), reader, caps))
			: undefined;
	const grow = modelsOn(config, 'claude-cli').map((m) => ({ value: m.id, label: m.label }));
	return {
		askModels: {
			choices: config.models.map((m) => ({ value: m.id, label: m.label })),
			default: config.ask.defaultModel
		},
		askWeb: webMode(config),
		growModels: config.grow ? { choices: grow, default: config.grow.defaultModel } : null,
		...(budget ? { budget } : {})
	};
}

export type AiOffered = Awaited<ReturnType<typeof offerFor>> | null;
