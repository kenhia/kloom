import { execFileSync } from 'node:child_process';
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

export default defineConfig({
	define: { __KLOOM_BUILD__: JSON.stringify(build()) },
	// SvelteKit's dev server serves only its own directories; a module the
	// engine imports lazily (the 3D view) is requested on its own, so the
	// engine is allowed too.
	server: { fs: { allow: ['engine'] } },
	plugins: [
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
					include: ['{src,engine}/**/*.{test,spec}.{js,ts}']
				}
			}
		]
	}
});
