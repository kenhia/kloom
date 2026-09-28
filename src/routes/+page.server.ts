import { loadAppConfig, webMode } from '$lib/server/app-config';
import { servedSubject } from '$lib/server/subject';
import type { PageServerLoad } from './$types';

// Read per request, so content written to disk, and a model renamed in the
// app config, show without a rebuild.
export const load: PageServerLoad = async () => {
	const [subject, config] = await Promise.all([servedSubject(), loadAppConfig()]);
	return {
		subject,
		askModels: {
			choices: config.models.map((m) => ({ value: m.id, label: m.label })),
			default: config.ask.defaultModel
		},
		askWeb: webMode(config),
		growModels: config.grow
			? {
					choices: config.models.map((m) => ({ value: m.id, label: m.label })),
					default: config.grow.defaultModel
				}
			: null
	};
};
