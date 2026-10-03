import { describe, expect, it } from 'vitest';
import { cliEnv } from '$engine/ai/claude-cli';
import { apiKey } from './api-key';

describe('the API key (korg 3529)', () => {
	const file = 'FLY_API_TOKEN=fly\nexport ANTHROPIC_API_KEY="sk-ant-file"\nOTHER=x\n';
	const read = () => file;

	it('comes from the environment first, then that one key from the file', () => {
		const p = { keyFile: '/etc/khomelab/secrets.env' };
		expect(apiKey(p, { ANTHROPIC_API_KEY: 'sk-ant-env' }, read)).toBe('sk-ant-env');
		expect(apiKey(p, {}, read)).toBe('sk-ant-file');
		expect(apiKey({ ...p, keyEnv: 'OTHER' }, {}, read)).toBe('x');
		expect(apiKey({ ...p, keyEnv: 'MISSING' }, {}, read)).toBeUndefined();
		expect(apiKey({}, {}, read)).toBeUndefined();
		expect(
			apiKey(p, {}, () => {
				throw new Error('EACCES');
			})
		).toBeUndefined();
	});

	it('never reaches claude -p, which would bill it instead of the subscription', () => {
		const env = cliEnv({ ANTHROPIC_API_KEY: 'k', ANTHROPIC_AUTH_TOKEN: 't', PATH: '/bin' });
		expect(env).toEqual({ PATH: '/bin' });
	});
});
