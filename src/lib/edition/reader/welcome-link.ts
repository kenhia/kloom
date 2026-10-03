import { fail, redirect, type Actions, type RequestEvent } from '@sveltejs/kit';
import { MIN_PASSWORD, passwordProblem } from '$lib/server/accounts';
import { accounts } from '$lib/server/reader-store';
import { setSession } from '$lib/server/session';

/**
 * A welcome link, `/welcome/<token>` (korg 3501): Ken mints it with the
 * admin CLI and texts it. Opening it only shows the form, so a message
 * app's link preview does not use it up; choosing a password does, signs
 * the reader in, and lands them on the Welcome and How-To page (3502).
 */
export const load = ({ params }: RequestEvent) => {
	const holder = accounts().invited(params.token ?? '');
	return { invited: holder ? { name: holder.displayName } : null, min: MIN_PASSWORD };
};

export const actions: Actions = {
	default: async ({ params, request, cookies }) => {
		const form = await request.formData();
		const password = String(form.get('password') ?? '');
		const confirm = String(form.get('confirm') ?? '');
		const problem = passwordProblem(password);
		if (problem) return fail(400, { message: problem });
		if (password !== confirm) return fail(400, { message: 'The two passwords are not the same.' });
		const accepted = await accounts().accept(params.token ?? '', password);
		if (!accepted)
			return fail(410, {
				message: 'This link has been used or has run out. Ask Ken for a new one.'
			});
		setSession(cookies, accepted.session);
		redirect(303, '/welcome');
	}
};
