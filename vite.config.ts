import { execFileSync } from 'node:child_process';
import { join, resolve, sep } from 'node:path';
import type { Plugin } from 'vite';
import { defineConfig } from 'vitest/config';
import adapter from '@sveltejs/adapter-node';
import { sveltekit } from '@sveltejs/kit/vite';

/** Which commit this build is, for the About panel: `<short hash> <date>`, or empty. */
function build(): string {
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

export default defineConfig({
	define: { __KLOOM_BUILD__: JSON.stringify(build()) },
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
			adapter: adapter(),
			// The engine lives beside src/, not inside it, so extracting the
			// framework later is moving a directory rather than untangling one.
			alias: { $engine: 'engine' },
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
