// The reader edition's providers: the Claude API only. `claude -p` is not in
// this build (korg 3500, 3530); a config naming it is refused, not run.
import { AnthropicApiProvider } from '$engine/ai/anthropic-api';
import type { Provider } from '$engine/ai/provider';
import { apiProvider } from '$lib/server/api-provider';
import type { AppConfig, ProviderConfig } from '$lib/server/app-config';

export function makeProvider(p: ProviderConfig, config: AppConfig): Provider {
	if (p.kind !== 'anthropic-api')
		throw new Error(`the reader edition runs only the Claude API, not ${p.kind}`);
	return apiProvider(p, config, AnthropicApiProvider);
}
