import type { AnthropicApiOptions, AnthropicApiProvider } from '$engine/ai/anthropic-api';
import { apiKey } from './api-key';
import { modelId, providerConfig, type ApiProviderConfig, type AppConfig } from './app-config';

/**
 * The API provider a config entry describes. The class is passed in, so
 * each edition's `providers` module names what it builds.
 */
export function apiProvider(
	p: ApiProviderConfig,
	config: AppConfig,
	Api: new (o: AnthropicApiOptions) => AnthropicApiProvider
): AnthropicApiProvider {
	const fallbacks = new Set(
		config.models
			.filter((m) => m.fallbacks && providerConfig(config, m.provider).id === p.id)
			.map(modelId)
	);
	return new Api({
		apiKey: () => apiKey(p),
		timeoutMs: p.timeoutSeconds * 1000,
		webTimeoutMs: (p.webTimeoutSeconds ?? 180) * 1000,
		web: {
			searchMaxUses: p.web?.searchMaxUses ?? 3,
			fetchMaxUses: p.web?.fetchMaxUses ?? 2,
			fetchMaxContentTokens: p.web?.fetchMaxContentTokens ?? 8000
		},
		fallbacks: (model) => fallbacks.has(model)
	});
}
