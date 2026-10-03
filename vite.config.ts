import { execFileSync } from 'node:child_process';
import { join, resolve, sep } from 'node:path';
import type { Plugin } from 'vite';
import { defineConfig } from 'vitest/config';
import adapter from '@sveltejs/adapter-node';
import { sveltekit } from '@sveltejs/kit/vite';

/**
 * Which commit this build is, for the About panel: `<short hash> <date>`, or
 * empty. `$KLOOM_BUILD` says so where there is no git, as in the public
 * site's image (Dockerfile).
 */
function build(): string {
	if (process.env.KLOOM_BUILD) return process.env.KLOOM_BUILD;
	try {
		return execFileSync('git', ['log', '-1', '--format=%h · %cs'], { encoding: 'utf8' }).trim();
	} catch {
		return '';
	}
}

/**
 * Tell the dev server's app when a subject or name file changes, so its
 * library (docs/design.md §Serving) rebuilds on the next read: Vite already
 * watches the repository, and a second watcher over every frame directory
 * cost the app 120 MB at five times today's content (sprint 032).
 */
function kloomContent(): Plugin {
	return {
		name: 'kloom-content',
		configureServer(server) {
			const subjects = resolve(process.env.KLOOM_SUBJECTS_DIR ?? 'subjects');
			const names = resolve(process.env.KLOOM_NAMES_DIR ?? join(subjects, '..', 'names'));
			server.watcher.add([subjects, names]);
			server.watcher.on('all', (_event, path) => {
				if ([subjects, names].some((d) => path.startsWith(d + sep)))
					process.emit('kloom:content-changed' as never);
			});
		}
	};
}

/**
 * Which edition this build is (docs/deploying.md §Editions, korg 3500):
 * `full`, the one on kai with ask, grow and keep, or `reader`, the public
 * site's, built with `KLOOM_EDITION=reader`. The reader edition is stripped,
 * not switched off: `$edition` resolves to its own modules, which hold no
 * agent code, and `__KLOOM_EDITION__` lets what is shared drop the rest.
 */
const edition = process.env.KLOOM_EDITION === 'reader' ? 'reader' : 'full';

/**
 * The reader edition's content security policy (korg 3501). Inline styles
 * stay allowed: the shell sets its palette and pane sizes as style
 * attributes. SvelteKit hashes its own inline script.
 */
const readerCsp = {
	mode: 'auto' as const,
	directives: {
		'default-src': ['self' as const],
		'script-src': ['self' as const],
		'style-src': ['self' as const, 'unsafe-inline' as const],
		'img-src': ['self' as const, 'data:' as const, 'blob:' as const],
		'font-src': ['self' as const, 'data:' as const],
		'connect-src': ['self' as const],
		'worker-src': ['self' as const, 'blob:' as const],
		'object-src': ['none' as const],
		'base-uri': ['self' as const],
		'form-action': ['self' as const],
		'frame-ancestors': ['none' as const]
	}
};

export default defineConfig({
	define: {
		__KLOOM_BUILD__: JSON.stringify(build()),
		__KLOOM_EDITION__: JSON.stringify(edition)
	},
	// SvelteKit's dev server serves only its own directories; a module the
	// engine imports lazily (the 3D view) is requested on its own, so the
	// engine is allowed too.
	// .scratch holds authors' checking copies of every subject, hundreds of
	// thousands of files nothing serves; watching them exhausted the system's
	// file watchers and the dev server would not start (sprint 028).
	server: { fs: { allow: ['engine'] }, watch: { ignored: ['**/.scratch/**'] } },
	plugins: [
		kloomContent(),
		sveltekit({
			compilerOptions: {
				// Keep dependencies' own compilation mode.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			// Each edition builds into its own directory, so building one never
			// replaces the other (`just build`, `just build-reader`).
			adapter: adapter({ out: edition === 'reader' ? 'build-reader' : 'build' }),
			// The engine lives beside src/, not inside it, so extracting the
			// framework later is moving a directory rather than untangling one.
			alias: { $engine: 'engine', $edition: `src/lib/edition/${edition}` },
			...(edition === 'reader' ? { csp: readerCsp } : {}),
			typescript: {
				config: (config) => {
					config.include.push('../engine/**/*.ts', '../engine/**/*.svelte');
				}
			}
		})
	],
	test: {
		expect: { requireAssertions: true },
		projects: [
			{
				extends: './vite.config.ts',
				test: {
					name: 'server',
					environment: 'node',
					globalSetup: ['./vitest.content.ts'],
					include: ['{src,engine}/**/*.{test,spec}.{js,ts}']
				}
			}
		]
	}
});
