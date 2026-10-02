// The content benchmark (korg 3460; docs/design.md §Serving): the library
// copied N times over, then compiled and served, measured against the
// targets. Run with `just bench` (N = 5); the numbers go in the sprint record.
//
//   node bench/content.mjs [--times 5] [--app build] [--skip-copy] [--keep-data] [--port 4899]
//
// --app names a built app (adapter-node's `build/`), so the same copy can be
// served by another commit's build for a before/after. The copy is made under
// .scratch/bench/x<N>: subject ids, name ids and Wikidata ids get a `-k<i>`
// suffix per copy (the first copy keeps the originals), and connections,
// marks and homes are renamed to match, so the copy links within itself as
// the library does. Media are hard links, so the copy costs little disk.
import { spawn } from 'node:child_process';
import {
	existsSync,
	linkSync,
	mkdirSync,
	readdirSync,
	readFileSync,
	rmSync,
	statSync,
	writeFileSync
} from 'node:fs';
import { request } from 'node:http';
import { join, resolve } from 'node:path';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
	const i = args.indexOf(`--${name}`);
	return i >= 0 ? args[i + 1] : fallback;
};
const times = Number(opt('times', '5'));
const app = resolve(opt('app', 'build'));
const port = Number(opt('port', '4899'));
const root = resolve('.scratch', 'bench', `x${times}`);
const subjects = join(root, 'subjects');
const names = join(root, 'names');
const data = join(root, `data-${port}`);

const suffix = (k) => (k === 1 ? '' : `-k${k}`);
const SUBJECT_REF = /^([a-z0-9][a-z0-9-]*)\/([\w-]+)$/;

/** Copy the library `times` times over, renamed so each copy links within itself. */
function copyLibrary() {
	rmSync(root, { recursive: true, force: true });
	mkdirSync(subjects, { recursive: true });
	mkdirSync(names, { recursive: true });
	const ids = readdirSync('subjects').filter((d) =>
		existsSync(join('subjects', d, 'subject.json'))
	);
	const nameIds = readdirSync('names')
		.filter((f) => f.endsWith('.json'))
		.map((f) => f.slice(0, -5));
	for (let k = 1; k <= times; k++) {
		const s = suffix(k);
		const ref = (to) => to.replace(SUBJECT_REF, (_, subj, frame) => `${subj}${s}/${frame}`);
		for (const id of ids) {
			const walk = (from, to) => {
				mkdirSync(to, { recursive: true });
				for (const e of readdirSync(from, { withFileTypes: true })) {
					const a = join(from, e.name);
					const b = join(to, e.name);
					if (e.isDirectory()) walk(a, b);
					else if (e.name === 'frame.json') {
						const f = JSON.parse(readFileSync(a, 'utf8'));
						for (const c of f.connections ?? []) c.to = ref(c.to);
						writeFileSync(b, JSON.stringify(f, null, '\t'));
					} else if (e.name === 'subject.json' && k > 1) {
						const m = JSON.parse(readFileSync(a, 'utf8'));
						m.title = `${m.title} (${k})`;
						writeFileSync(b, JSON.stringify(m, null, '\t'));
					} else if (e.name.endsWith('.md') && k > 1)
						writeFileSync(
							b,
							readFileSync(a, 'utf8').replace(/kloom:e\/([a-z0-9-]+)/g, `kloom:e/$1${s}`)
						);
					else linkSync(a, b);
				}
			};
			walk(join('subjects', id), join(subjects, `${id}${s}`));
		}
		for (const id of nameIds) {
			const n = JSON.parse(readFileSync(join('names', `${id}.json`), 'utf8'));
			n.id = `${id}${s}`;
			if (k > 1 && n.wikidata) n.wikidata = `${n.wikidata}00000${k}`;
			if (n.home) n.home = ref(n.home);
			writeFileSync(join(names, `${id}${s}.json`), JSON.stringify(n, null, '\t'));
		}
	}
}

/** Bytes and size of a directory. */
function sizeOf(dir) {
	let files = 0;
	let bytes = 0;
	const walk = (d) => {
		for (const e of readdirSync(d, { withFileTypes: true })) {
			if (e.isDirectory()) walk(join(d, e.name));
			else {
				files++;
				bytes += statSync(join(d, e.name)).size;
			}
		}
	};
	walk(dir);
	return { files, bytes };
}

/** One GET, timed: time to first byte and to the end, and the bytes on the wire. */
function get(path, encoding = 'identity') {
	return new Promise((done, fail) => {
		const start = performance.now();
		let ttfb = 0;
		const req = request(
			{
				host: '127.0.0.1',
				port,
				path,
				headers: { 'accept-encoding': encoding, accept: 'text/html,*/*' }
			},
			(res) => {
				ttfb = performance.now() - start;
				let bytes = 0;
				res.on('data', (c) => (bytes += c.length));
				res.on('end', () =>
					done({
						status: res.statusCode,
						bytes,
						ttfb,
						total: performance.now() - start,
						headers: res.headers
					})
				);
			}
		);
		req.on('error', fail);
		req.end();
	});
}

const median = (xs) => [...xs].sort((a, b) => a - b)[Math.floor(xs.length / 2)];
const p95 = (xs) => [...xs].sort((a, b) => a - b)[Math.floor(xs.length * 0.95)];
const ms = (x) => `${x.toFixed(1)} ms`;
const kb = (x) => `${(x / 1024).toFixed(0)} KB`;

async function main() {
	if (!args.includes('--skip-copy')) {
		const t = performance.now();
		copyLibrary();
		console.error(`copied the library ×${times} in ${ms(performance.now() - t)}`);
	}
	const src = sizeOf(subjects);
	const nm = sizeOf(names);
	// --keep-data serves the library the last run built, so the server starts without building it.
	if (!args.includes('--keep-data')) rmSync(data, { recursive: true, force: true });
	mkdirSync(data, { recursive: true });
	const contentDb = join(data, 'content.db');

	const env = {
		...process.env,
		PORT: String(port),
		HOST: '127.0.0.1',
		KLOOM_SUBJECTS_DIR: subjects,
		KLOOM_NAMES_DIR: names,
		KLOOM_DATA_DIR: data,
		KLOOM_CONTENT_DB: contentDb,
		KLOOM_SUBJECT: 'western-civ'
	};
	const started = performance.now();
	const server = spawn(process.execPath, [join(app, 'index.js')], {
		env,
		cwd: resolve(app, '..'),
		stdio: ['ignore', 'pipe', 'pipe']
	});
	let log = '';
	server.stdout.on('data', (c) => (log += c));
	server.stderr.on('data', (c) => (log += c));
	try {
		// Up when the landing page answers; the first request builds the library.
		let first;
		for (let i = 0; i < 600; i++) {
			first = await get('/western-civ').catch(() => null);
			if (first?.status === 200) break;
			await new Promise((r) => setTimeout(r, 200));
		}
		if (first?.status !== 200) throw new Error(`the server did not come up:\n${log}`);
		const ready = performance.now() - started;
		const built = /content: built [^\n]* in (\d+) ms/.exec(log);

		const ids = readdirSync(subjects).sort();
		const rows = [];
		for (const id of ['western-civ', 'physics', 'ai', `physics${suffix(times)}`]) {
			const page = `/${id}`;
			await get(page); // warm
			const raw = [];
			const br = [];
			const gz = [];
			for (let i = 0; i < 5; i++) {
				raw.push(await get(page));
				br.push(await get(page, 'br'));
				gz.push(await get(page, 'gzip'));
			}
			rows.push({
				page,
				raw: raw[0].bytes,
				gzip: gz[0].bytes,
				br: br[0].bytes,
				encoded: br[0].headers['content-encoding'] ?? 'none',
				ttfb: median(br.map((r) => r.ttfb)),
				total: median(br.map((r) => r.total))
			});
		}

		// A frame step: each frame's body, as the shell fetches it ahead.
		const steps = [];
		const sizes = [];
		let frameApi = true;
		for (const id of ids.filter((_, i) => i % Math.max(1, Math.floor(ids.length / 10)) === 0)) {
			const spine = JSON.parse(readFileSync(join(subjects, id, 'spine.json'), 'utf8'));
			const frames = spine.segments.flatMap((s) => s.frames).slice(0, 12);
			for (const f of frames) {
				const r = await get(`/api/frame/${id}/${f}`, 'br');
				if (r.status === 404) frameApi = false;
				steps.push(r.total);
				sizes.push(r.bytes);
			}
		}

		const timed = async (path, n = 10) => {
			await get(path, 'br');
			const rs = [];
			for (let i = 0; i < n; i++) rs.push(await get(path, 'br'));
			const raw = await get(path);
			return { total: median(rs.map((r) => r.total)), bytes: rs[0].bytes, raw: raw.bytes };
		};
		const map = await timed('/api/map');
		const stats = await timed('/api/stats');
		const start = await timed(`/api/start/physics${suffix(times)}`);

		const status = readFileSync(`/proc/${server.pid}/status`, 'utf8');
		const rss = Number(/VmRSS:\s+(\d+)/.exec(status)[1]) * 1024;
		const hwm = Number(/VmHWM:\s+(\d+)/.exec(status)[1]) * 1024;
		const db = existsSync(contentDb) ? statSync(contentDb).size : null;

		const out = [];
		out.push(`## Content benchmark ×${times} (${app})`, '');
		out.push(
			`Library: ${ids.length} subjects, ${src.files.toLocaleString()} files, ${(src.bytes / 2 ** 20).toFixed(0)} MB; ${nm.files.toLocaleString()} names.`
		);
		out.push(
			`Server up and first page served in ${ms(ready)}` +
				(built ? `; the library built in ${built[1]} ms` : '') +
				(db ? `; content.db ${(db / 2 ** 20).toFixed(0)} MB.` : '.'),
			''
		);
		out.push(
			'| Page | Raw | gzip | Brotli | Sent as | TTFB | Total |',
			'| --- | ---: | ---: | ---: | --- | ---: | ---: |'
		);
		for (const r of rows)
			out.push(
				`| \`${r.page}\` | ${kb(r.raw)} | ${kb(r.gzip)} | ${kb(r.br)} | ${r.encoded} | ${ms(r.ttfb)} | ${ms(r.total)} |`
			);
		out.push('');
		if (frameApi)
			out.push(
				`Frame step (\`/api/frame\`, ${steps.length} frames): median ${ms(median(steps))}, p95 ${ms(p95(steps))}, median ${kb(median(sizes))} on the wire.`
			);
		else out.push('Frame step: this build has no frame endpoint (every page carries every frame).');
		out.push(
			`Map (\`/api/map\`): ${ms(map.total)}, ${kb(map.bytes)} sent (${kb(map.raw)} raw).`,
			`Stats (\`/api/stats\`): ${ms(stats.total)}. Start look: ${ms(start.total)}.`,
			`Server memory: ${(rss / 2 ** 20).toFixed(0)} MB resident, ${(hwm / 2 ** 20).toFixed(0)} MB peak.`
		);
		console.log(out.join('\n'));
	} finally {
		server.kill();
	}
}

await main();
