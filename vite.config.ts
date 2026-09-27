import { defineConfig } from 'vitest/config';
import adapter from '@sveltejs/adapter-node';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
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
