import { fail, redirect, type Actions, type RequestEvent } from '@sveltejs/kit';
import { usernameOf } from '$lib/server/accounts';
import { RateLimit, signInLimits } from '$lib/server/rate-limit';
import { accounts } from '$lib/server/reader-store';
import { clientAddress, safeNext, setSession } from '$lib/server/session';

/**
 * Signing in with a username and password (korg 3501), for a device the
 * reader's welcome link was not opened on. Failures back off per username
 * and per address (rate-limit.ts).
 */
const byUser = new RateLimit(signInLimits.user);
const byAddress = new RateLimit(signInLimits.address);

export const load = ({ locals, url }: RequestEvent) => {
	const next = safeNext(url.searchParams.get('next'));
	if (locals.reader) redirect(303, next);
	return { next };
};

export const actions: Actions = {
	default: async (event) => {
		const form = await event.request.formData();
		const username = String(form.get('username') ?? '').trim();
		const password = String(form.get('password') ?? '');
		const next = safeNext(String(form.get('next') ?? ''));
		const user = [`user ${usernameOf(username) ?? username.toLowerCase()}`];
		const address = [`address ${clientAddress(event)}`];

		const wait = Math.max(byUser.wait(user), byAddress.wait(address));
		if (wait) {
			const minutes = Math.ceil(wait / 60_000);
			return fail(429, {
				username,
				message: `Too many tries. Wait ${minutes === 1 ? 'a minute' : `${minutes} minutes`} and try again.`
			});
		}
		const signed = username && password ? await accounts().signIn(username, password) : null;
		if (!signed) {
			byUser.fail(user);
			byAddress.fail(address);
			return fail(400, { username, message: 'That username and password do not match.' });
		}
		byUser.succeed(user);
		setSession(event.cookies, signed.session);
		redirect(303, next);
	}
};
