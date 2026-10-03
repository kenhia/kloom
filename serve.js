// kloom's production server (docs/deploying.md): the adapter-node handler
// behind the listeners its edition is for.
//
// The full edition (`npm run build` → build/), on kai: two loopback
// listeners, one per door (src/lib/server/reader.ts).
//
//   $KLOOM_TAILNET_PORT (4890)  fronted by `tailscale serve`; writes need the
//                               tailnet identity serve injects
//   $KLOOM_LOCAL_PORT   (4891)  for ssh forwards; trusted as the host's user
//
// Both bind 127.0.0.1 and so look alike to the app. Each request is marked
// with its door and a key made here, at start, overwriting any mark a client
// sent; the app trusts no mark without the key.
//
// The reader edition (`just build-reader` → build-reader/), the public site:
// `KLOOM_EDITION=reader node serve.js` opens one listener on 0.0.0.0:$PORT
// (8080) with no doors at all. Who is reading comes from their session
// (src/lib/edition/reader/hooks.ts); that build has no door to mark.
//
// Run after building: `node serve.js`.
import { randomBytes } from 'node:crypto';
import { createServer } from 'node:http';

const reader = process.env.KLOOM_EDITION === 'reader';

const key = randomBytes(16).toString('hex');
if (!reader) process.env.KLOOM_DOOR_KEY = key;
else delete process.env.KLOOM_DOOR_KEY;

// Imported by URL so the gates need no build; the handler reads the env above.
// Each edition is its own build, so the mode cannot open the other's.
const build = reader ? './build-reader/handler.js' : './build/handler.js';
const { handler } = await import(new URL(build, import.meta.url).href);

let servers;
if (reader) {
	const port = Number(process.env.PORT ?? 8080);
	const host = process.env.HOST ?? '0.0.0.0';
	servers = [
		createServer((req, res) => {
			// No door here; a mark a client sent means nothing, and goes.
			delete req.headers['x-kloom-door'];
			handler(req, res);
		}).listen(port, host, () => console.log(`kloom: reader edition on ${host}:${port}`))
	];
} else {
	const doors = {
		tailnet: Number(process.env.KLOOM_TAILNET_PORT ?? 4890),
		local: Number(process.env.KLOOM_LOCAL_PORT ?? 4891)
	};
	servers = Object.entries(doors).map(([door, port]) =>
		createServer((req, res) => {
			req.headers['x-kloom-door'] = `${key} ${door}`;
			handler(req, res);
		}).listen(port, '127.0.0.1', () => console.log(`kloom: ${door} door on 127.0.0.1:${port}`))
	);
}

// systemd (or Fly) stops the process with SIGTERM; its control group takes any grow child with it.
for (const signal of ['SIGTERM', 'SIGINT'])
	process.once(signal, () => {
		for (const s of servers) s.close();
		process.exit(0);
	});
