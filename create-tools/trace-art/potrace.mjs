// Traces a greyscale PNG with the npm `potrace` port and prints the SVG.
// Called by trace.py; `potrace` is resolved from the prefix it passes, so it
// never becomes a dependency of the app.
import { createRequire } from 'node:module';
import { join, resolve } from 'node:path';

const [prefix, input, threshold, turdSize, optTolerance] = process.argv.slice(2);
const require = createRequire(join(resolve(prefix), 'noop.js'));
const potrace = require('potrace');
potrace.trace(
	input,
	{
		threshold: Number(threshold),
		turdSize: Number(turdSize),
		optTolerance: Number(optTolerance),
		turnPolicy: potrace.Potrace.TURNPOLICY_MINORITY
	},
	(err, svg) => {
		if (err) throw err;
		process.stdout.write(svg);
	}
);
