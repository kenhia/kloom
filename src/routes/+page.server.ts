import { loadSubject } from '$engine/load';
import { loadAppConfig } from '$lib/server/app-config';
import { subjectDir } from '$lib/server/config';
import type { PageServerLoad } from './$types';

// Read per request, so content written to disk, and a model renamed in the
// app config, show without a rebuild.
export const load: PageServerLoad = async () => {
	const [subject, config] = await Promise.all([loadSubject(subjectDir()), loadAppConfig()]);
	return {
		subject,
		askModels: {
			choices: config.models.map((m) => ({ value: m.id, label: m.label })),
			default: config.ask.defaultModel
		}
	};
};
