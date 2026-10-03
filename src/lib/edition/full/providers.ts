// The full edition's providers: `claude -p` and the Claude API.
import { AnthropicApiProvider } from '$engine/ai/anthropic-api';
import { ClaudeCliProvider } from '$engine/ai/claude-cli';
import type { Provider } from '$engine/ai/provider';
import { apiProvider } from '$lib/server/api-provider';
import type { AppConfig, ProviderConfig } from '$lib/server/app-config';

/** Build the provider a config entry describes. */
export function makeProvider(p: ProviderConfig, config: AppConfig): Provider {
	if (p.kind === 'anthropic-api') return apiProvider(p, config, AnthropicApiProvider);
	return new ClaudeCliProvider({
		command: p.command,
		timeoutMs: p.timeoutSeconds * 1000,
		webTimeoutMs: (p.webTimeoutSeconds ?? 180) * 1000
	});
}
