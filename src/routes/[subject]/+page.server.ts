import { loadAppConfig, webMode } from '$lib/server/app-config';
import { listSubjects } from '$lib/server/config';
import { servedSubject } from '$lib/server/subject';
import type { PageServerLoad } from './$types';

// Read per request, so content written to disk, and a model renamed in the
// app config, show without a rebuild. An unknown subject is a 404.
export const load: PageServerLoad = async ({ params }) => {
	const [subject, config, subjects] = await Promise.all([
		servedSubject(params.subject),
		loadAppConfig(),
		listSubjects()
	]);
	return {
		subject,
		subjects,
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
