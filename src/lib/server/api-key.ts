import { readFileSync } from 'node:fs';
import type { ApiProviderConfig } from './app-config';

/**
 * The API provider's key (korg 3529), read per turn so a rotated key needs
 * no restart: from the environment (the reader site's Fly secret), else that
 * one key from a dotenv file (kai's `/etc/khomelab/secrets.env`). Only the
 * named key is taken; the rest of the file never reaches the app's
 * environment, nor `claude -p`'s.
 */
export function apiKey(
	p: Pick<ApiProviderConfig, 'keyEnv' | 'keyFile'>,
	env: NodeJS.ProcessEnv = process.env,
	read: (path: string) => string = (path) => readFileSync(path, 'utf8')
): string | undefined {
	const name = p.keyEnv ?? 'ANTHROPIC_API_KEY';
	if (env[name]) return env[name];
	if (!p.keyFile) return undefined;
	let text: string;
	try {
		text = read(p.keyFile);
	} catch {
		return undefined;
	}
	for (const line of text.split('\n')) {
		const m = /^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/.exec(line);
		if (m?.[1] !== name) continue;
		const value = m[2].replace(/^(['"])(.*)\1$/, '$2');
		return value || undefined;
	}
	return undefined;
}
