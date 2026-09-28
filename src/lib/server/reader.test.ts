import { describe, expect, it } from 'vitest';
import { DOOR_HEADER, doorOf, isWrite, readerOf } from './reader';

const KEY = '0123456789abcdef';
const h = (o: Record<string, string>) => new Headers(o);

describe('doorOf', () => {
	it('names the door serve.js marked, with its key', () => {
		expect(doorOf(h({ [DOOR_HEADER]: `${KEY} tailnet` }), KEY)).toBe('tailnet');
		expect(doorOf(h({ [DOOR_HEADER]: `${KEY} local` }), KEY)).toBe('local');
	});

	it('is no door without serve.js, or with a guessed key', () => {
		expect(doorOf(h({ [DOOR_HEADER]: `${KEY} local` }), undefined)).toBeNull();
		expect(doorOf(h({ [DOOR_HEADER]: 'guess local' }), KEY)).toBeNull();
		expect(doorOf(h({ [DOOR_HEADER]: `${KEY} front` }), KEY)).toBeNull();
		expect(doorOf(h({}), KEY)).toBeNull();
	});
});

describe('readerOf', () => {
	const serve = {
		'tailscale-user-login': 'ken@github',
		'tailscale-user-name': 'Ken Hiatt'
	};

	it('takes the tailnet identity serve injected', () => {
		expect(readerOf(h(serve), 'tailnet', false, 'ken@kai')).toEqual({
			login: 'ken@github',
			name: 'Ken Hiatt',
			via: 'tailscale-serve'
		});
	});

	it('refuses a tailnet request that carries no identity (a tagged node)', () => {
		expect(readerOf(h({}), 'tailnet', false, 'ken@kai')).toBeNull();
		expect(readerOf(h({ 'tailscale-user-login': ' ' }), 'tailnet', false, 'ken@kai')).toBeNull();
	});

	it('falls back to the login for a name serve encoded or left out', () => {
		const encoded = { ...serve, 'tailscale-user-name': '=?utf-8?q?J=C3=B6rg?=' };
		expect(readerOf(h(encoded), 'tailnet', false, 'x')?.name).toBe('ken@github');
		expect(readerOf(h({ 'tailscale-user-login': 'a@b' }), 'tailnet', false, 'x')?.name).toBe('a@b');
	});

	it('trusts the ssh door as the local login, and ignores identity headers there', () => {
		expect(readerOf(h(serve), 'local', false, 'ken@kai')).toEqual({
			login: 'ken@kai',
			name: 'ken@kai',
			via: 'ssh'
		});
	});

	it('trusts the dev server, and nothing else without a door', () => {
		expect(readerOf(h({}), null, true, 'ken@kai')?.via).toBe('dev');
		expect(readerOf(h(serve), null, false, 'ken@kai')).toBeNull();
	});
});

describe('isWrite', () => {
	it('is every request that is not a read, wherever it goes', () => {
		for (const m of ['POST', 'PUT', 'PATCH', 'DELETE']) expect(isWrite(m)).toBe(true);
		for (const m of ['GET', 'HEAD', 'OPTIONS']) expect(isWrite(m)).toBe(false);
	});
});
