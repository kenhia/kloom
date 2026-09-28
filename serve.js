// kloom's production server (docs/deploying.md): the adapter-node handler
// behind two loopback listeners, one per door (src/lib/server/reader.ts).
//
//   $KLOOM_TAILNET_PORT (4890)  fronted by `tailscale serve`; writes need the
//                               tailnet identity serve injects
//   $KLOOM_LOCAL_PORT   (4891)  for ssh forwards; trusted as the host's user
//
// Both bind 127.0.0.1 and so look alike to the app. Each request is marked
// with its door and a key made here, at start, overwriting any mark a client
// sent; the app trusts no mark without the key.
//
// Run after `npm run build`: `node serve.js`.
import { randomBytes } from 'node:crypto';
import { createServer } from 'node:http';

const key = randomBytes(16).toString('hex');
process.env.KLOOM_DOOR_KEY = key;

// Imported by URL so the gates need no build; the handler reads the env above.
const { handler } = await import(new URL('./build/handler.js', import.meta.url).href);

const doors = {
	tailnet: Number(process.env.KLOOM_TAILNET_PORT ?? 4890),
	local: Number(process.env.KLOOM_LOCAL_PORT ?? 4891)
};

const servers = Object.entries(doors).map(([door, port]) =>
	createServer((req, res) => {
		req.headers['x-kloom-door'] = `${key} ${door}`;
		handler(req, res);
	}).listen(port, '127.0.0.1', () => console.log(`kloom: ${door} door on 127.0.0.1:${port}`))
);

// systemd stops the unit with SIGTERM; its control group takes any grow child with it.
for (const signal of ['SIGTERM', 'SIGINT'])
	process.once(signal, () => {
		for (const s of servers) s.close();
		process.exit(0);
	});
