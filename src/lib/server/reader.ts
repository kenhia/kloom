import { hostname, userInfo } from 'node:os';
import { env } from '$env/dynamic/private';

/**
 * Who is making a request (korg 3384, 3388; docs/deploying.md). The service
 * binds loopback only and has two doors, both opened by `serve.js`:
 *
 * - **tailnet** — the port `tailscale serve` fronts. Serve strips any
 *   `Tailscale-User-*` header a client sends and injects the signed-in
 *   user's, so the header is the identity. A tagged node gets none.
 * - **local** — the port kept for ssh forwards (kwork's demos). Reaching it
 *   took an ssh login on the host, so the caller is trusted as the host's
 *   own user, and any identity header is ignored.
 *
 * Both arrive from 127.0.0.1, so the peer address cannot tell them apart:
 * `serve.js` marks each request with the door it came in by and a key only
 * this process knows. With no mark, only the dev server is trusted.
 */

export interface Reader {
	/** `ken@github` from serve, or the host's `user@host` for the other two. */
	login: string;
	name: string;
	via: 'tailscale-serve' | 'ssh' | 'dev';
}

export type Door = 'tailnet' | 'local';

/** Set by `serve.js` on every request, overwriting whatever a client sent. */
export const DOOR_HEADER = 'x-kloom-door';

/** The door a request came in by, or null when `serve.js` did not mark it with `key`. */
export function doorOf(headers: Headers, key: string | undefined): Door | null {
	const mark = headers.get(DOOR_HEADER);
	if (!key || !mark) return null;
	const [k, door] = mark.split(' ');
	return k === key && (door === 'tailnet' || door === 'local') ? door : null;
}

/** The host's own user, for the ssh door and the dev server. */
export const localLogin = () => env.KLOOM_LOCAL_LOGIN || `${userInfo().username}@${hostname()}`;

/** Who is asking, or null when nobody may write. */
export function readerOf(
	headers: Headers,
	door: Door | null,
	dev: boolean,
	local: string
): Reader | null {
	if (door === 'tailnet') {
		const login = headers.get('tailscale-user-login')?.trim();
		if (!login) return null;
		const name = headers.get('tailscale-user-name')?.trim();
		// Serve MIME-encodes a name that is not ASCII; the login says it well enough.
		return { login, name: name && !name.startsWith('=?') ? name : login, via: 'tailscale-serve' };
	}
	if (door === 'local') return { login: local, name: local, via: 'ssh' };
	return dev ? { login: local, name: local, via: 'dev' } : null;
}

/** Ask, keep and grow are POSTs; every request that is not a read needs a reader. */
export const isWrite = (method: string) => !['GET', 'HEAD', 'OPTIONS'].includes(method);
