<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import type { ConfigOptions, ForceGraph3DInstance } from '3d-force-graph';
	import type { BufferGeometry, Material, PerspectiveCamera } from 'three';
	import { library3dOf, type Link3d, type Node3d } from '../library3d';
	import { subjectSlot, type MapData, type MapTarget, type Shape } from '../map';

	/**
	 * The library in 3D (docs/design.md §The library in 3D, korg 3449): every
	 * frame, name and connection as a WebGL force graph, turned with the
	 * pointer. Decorative, and said so: the 2D map and its list are the way to
	 * read the graph, and this view links to them. three.js arrives only when
	 * this view opens (the overlay imports this component lazily, and this
	 * component imports the graph lazily again).
	 */
	interface Props {
		data: MapData;
		/** The frame the reader is on (`<subject>/<frame>`), picked at the start. */
		here?: string | null;
		/** Any frame's address; the page resolves it. */
		hrefOf: (key: string) => string;
		/** Go to a frame: the map closes, and the page jumps. */
		onfollow: (key: string) => void;
		/** The same node on the 2D map. */
		onshow2d: (target: MapTarget) => void;
	}

	let { data, here = null, hrefOf, onfollow, onshow2d }: Props = $props();

	const lib = untrack(() => library3dOf(data));
	const byId: Record<string, Node3d> = Object.fromEntries(lib.nodes.map((n) => [n.id, n]));

	let host = $state<HTMLElement>();
	let stage = $state<HTMLElement>();
	let width = $state(0);
	let height = $state(0);
	let status = $state<'loading' | 'ready' | 'failed'>('loading');
	let selected = $state<Node3d | null>(untrack(() => (here ? (byId[`f:${here}`] ?? null) : null)));
	/** Turning on its own: never under reduced motion, and the reader can stop it (WCAG 2.2.2). */
	let turning = $state(false);
	let reduced = $state(false);

	/** What the graph library holds for a node and a link once it has laid them out. */
	type GNode = Node3d & { x?: number; y?: number; z?: number };
	type GLink = Omit<Link3d, 'source' | 'target'> & {
		source: string | GNode;
		target: string | GNode;
	};
	let graph: ForceGraph3DInstance<GNode, GLink> | null = null;
	/** Its constructor, typed for these nodes and links (the package does not export its own). */
	type Graph3d = new (
		element: HTMLElement,
		options?: ConfigOptions
	) => ForceGraph3DInstance<GNode, GLink>;
	let controls: { autoRotate: boolean; autoRotateSpeed: number } | null = null;
	/** Set once the reader turns, zooms or picks: the camera is theirs from then on. */
	let held = false;
	/** The node under the pointer: its links come forward. */
	let hot: string | null = null;

	const fmt = (n: number) => n.toLocaleString('en');
	const endId = (e: string | GNode) => (typeof e === 'string' ? e : e.id);
	const lit = (l: GLink) => !!hot && (endId(l.source) === hot || endId(l.target) === hot);
	const escape = (s: string) =>
		s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);

	function setTurning(on: boolean) {
		turning = on;
		if (controls) controls.autoRotate = on;
	}

	/**
	 * Take in the whole library: the camera faces the middle of the frames, as
	 * far back as fits their width and height at that depth. (The graph
	 * library's own fit takes in the nearest points too, which leaves the
	 * library a small knot in the middle.)
	 */
	function fit(g: ForceGraph3DInstance<GNode, GLink>, ms: number) {
		const b = g.getGraphBbox((n) => n.kind === 'frame');
		const camera = g.camera() as PerspectiveCamera;
		if (!b || !camera.fov) return;
		const [cx, cy, cz] = [b.x, b.y, b.z].map(([lo, hi]) => (lo + hi) / 2);
		const half = Math.max((b.y[1] - b.y[0]) / 2, (b.x[1] - b.x[0]) / 2 / camera.aspect);
		const d = (half * 1.05) / Math.tan((camera.fov * Math.PI) / 360);
		g.cameraPosition({ x: cx, y: cy, z: cz + d }, { x: cx, y: cy, z: cz }, ms);
	}

	/** Fly to a node and say what it is. */
	function pick(n: GNode) {
		selected = byId[n.id] ?? null;
		held = true;
		setTurning(false);
		if (!graph) return;
		const { x = 0, y = 0, z = 0 } = n;
		const k = 1 + 90 / (Math.hypot(x, y, z) || 1);
		graph.cameraPosition({ x: x * k, y: y * k, z: z * k }, { x, y, z }, reduced ? 0 : 1200);
	}

	onMount(() => {
		reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
		let gone = false;
		const disposables: { dispose(): void }[] = [];
		/** One per colour, made as the nodes are drawn; disposed with the view. */
		const materials: Record<string, Material> = {};
		(async () => {
			try {
				const [{ default: ForceGraph3D }, THREE] = await Promise.all([
					import('3d-force-graph'),
					import('three')
				]);
				if (gone || !stage || !host) return;
				// The map's own surface and subject colours, in the light it opened in.
				const css = getComputedStyle(host);
				const color = (v: string) => css.getPropertyValue(v).trim() || '#888';
				const ink = color('--map-ink');
				const line = color('--map-line');
				const muted = color('--map-muted');

				// A solid for each subject's 2D shape, so colour is never the only cue.
				const solids: Record<Shape, BufferGeometry> = {
					circle: new THREE.SphereGeometry(1, 16, 12),
					square: new THREE.BoxGeometry(1.6, 1.6, 1.6),
					diamond: new THREE.OctahedronGeometry(1.3),
					triangle: new THREE.TetrahedronGeometry(1.5),
					hexagon: new THREE.CylinderGeometry(1, 1, 1.2, 6),
					star: new THREE.IcosahedronGeometry(1.25),
					other: new THREE.SphereGeometry(1, 16, 12)
				};
				const nameSolid = new THREE.SphereGeometry(1, 8, 6);
				const material = (c: string) =>
					(materials[c] ??= new THREE.MeshLambertMaterial({ color: c }));
				disposables.push(...Object.values(solids), nameSolid);

				const object = (n: GNode) => {
					if (n.kind === 'name') {
						const m = new THREE.Mesh(nameSolid, material(color('--map-other')));
						m.scale.setScalar(1.2 + Math.sqrt(n.degree) * 0.18);
						return m;
					}
					const s = subjectSlot(data, n.subject!);
					const m = new THREE.Mesh(
						solids[s.shape],
						material(s.slot ? color(`--map-s${s.slot}`) : color('--map-other'))
					);
					m.scale.setScalar(2.4 + Math.sqrt(n.degree) * 0.9);
					return m;
				};

				const g = new (ForceGraph3D as unknown as Graph3d)(stage, { controlType: 'orbit' })
					.width(width)
					.height(height)
					.backgroundColor(color('--map-surface'))
					.showNavInfo(false)
					.nodeThreeObject(object)
					.nodeLabel(
						(n) =>
							`<strong>${escape(n.label)}</strong><br><span>${escape(n.kind === 'name' ? 'A name' : n.detail)}</span>`
					)
					.linkColor((l) => (lit(l) ? ink : l.kind === 'connection' ? muted : line))
					.linkOpacity(0.55)
					.linkDirectionalParticles((l) => (!reduced && lit(l) ? 2 : 0))
					.linkDirectionalParticleWidth(1.5)
					.linkDirectionalParticleColor(() => ink)
					.onNodeHover((n) => {
						hot = n?.id ?? null;
						if (stage) stage.style.cursor = n ? 'pointer' : '';
						g.linkColor(g.linkColor()).linkDirectionalParticles(g.linkDirectionalParticles());
					})
					.onNodeClick(pick)
					.enableNodeDrag(false);
				// Laid out before the first paint (about half a second). Under reduced
				// motion it stops there, and the camera takes in the whole library at
				// once; otherwise it drifts on to rest, and the camera then eases out to
				// the whole of it, unless the reader has taken hold of it by then.
				g.warmupTicks(160);
				if (reduced) g.cooldownTicks(0);
				else g.cooldownTime(4000);
				// The nodes are moved into place just after this is called, and the fit
				// reads their world matrices, which only a render updates: so fit on the
				// next frame, with the matrices brought up to date first.
				let framed = false;
				g.onEngineTick(() => {
					if (framed) return;
					framed = true;
					requestAnimationFrame(() => {
						if (held || gone) return;
						g.scene().updateMatrixWorld(true);
						fit(g, 0);
					});
				});
				g.onEngineStop(() =>
					requestAnimationFrame(() => {
						if (held || gone) return;
						g.scene().updateMatrixWorld(true);
						fit(g, reduced ? 0 : 800);
					})
				);
				g.graphData({
					nodes: lib.nodes.map((n) => ({ ...n })),
					links: lib.links.map((l) => ({ ...l }))
				});
				controls = g.controls() as typeof controls;
				if (controls) controls.autoRotateSpeed = 0.6;
				// Taking hold of the graph stops it turning.
				(
					g.controls() as EventTarget & { addEventListener: (t: string, f: () => void) => void }
				).addEventListener?.('start', () => {
					held = true;
					setTurning(false);
				});
				setTurning(!reduced);
				graph = g;
				status = 'ready';
			} catch (e) {
				console.warn('3D: could not start', e);
				status = 'failed';
			}
		})();
		return () => {
			gone = true;
			graph?._destructor();
			graph = null;
			for (const d of [...disposables, ...Object.values(materials)]) d.dispose();
		};
	});

	$effect(() => {
		if (status === 'ready' && width && height) graph?.width(width).height(height);
	});

	const shown2d = (n: Node3d): MapTarget =>
		n.kind === 'frame'
			? { view: 'frame', key: n.id.slice(2), steps: 2 }
			: { view: 'name', id: n.id.slice(2) };

	function go(e: MouseEvent, key: string) {
		if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		onfollow(key);
	}
</script>

<div class="library3d" bind:this={host}>
	<!-- Drawn for the eye: the counts below and the 2D map say what it holds. -->
	<div
		class="stage"
		aria-hidden="true"
		bind:this={stage}
		bind:clientWidth={width}
		bind:clientHeight={height}
	></div>
	{#if status !== 'ready'}
		<p class="empty" role="status">
			{status === 'loading'
				? 'Loading the 3D view…'
				: 'The 3D view needs WebGL, which this browser did not give it. The 2D map has everything it shows.'}
		</p>
	{/if}

	<div class="info">
		<div class="top">
			<p class="summary">
				The whole library: {fmt(lib.totals.frames)} frames in {lib.subjects.length} subjects,
				{fmt(lib.totals.names)} names and {fmt(lib.totals.connections)} connections, with
				{fmt(lib.totals.mentions)} lines from frames to the names they mention.
			</p>
			{#if !reduced && status === 'ready'}
				<p class="actions">
					<button type="button" aria-pressed={turning} onclick={() => setTurning(!turning)}>
						Turn slowly
					</button>
				</p>
			{/if}
		</div>
		<details>
			<summary>Counts by subject</summary>
			<table>
				<caption class="visually-hidden">The library in 3D, by subject</caption>
				<thead>
					<tr>
						<th scope="col">Subject</th>
						<th scope="col">Frames</th>
						<th scope="col">Connections</th>
						<th scope="col">Names</th>
					</tr>
				</thead>
				<tbody>
					{#each lib.subjects as s (s.id)}
						<tr>
							<th scope="row">{s.title}</th>
							<td>{fmt(s.frames)}</td>
							<td>{fmt(s.connections)}</td>
							<td>{fmt(s.names)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</details>

		<div class="details" aria-live="polite">
			{#if selected}
				<p class="what">
					<strong>{selected.label}</strong>
					<span class="context"
						>{selected.kind === 'name' ? 'A name' : selected.detail}{selected.id === `f:${here}`
							? ' · you are here'
							: ''}</span
					>
				</p>
				{#if selected.kind === 'name'}<p class="why">{selected.detail}</p>{/if}
				<p class="actions">
					{#if selected.kind === 'frame'}
						{@const key = selected.id.slice(2)}
						<!-- The page resolved this app route. -->
						<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
						<a href={hrefOf(key)} onclick={(e) => go(e, key)}>Go to {selected.label}</a>
					{/if}
					<button type="button" onclick={() => onshow2d(shown2d(selected!))}>
						Show on the 2D map
					</button>
				</p>
			{:else}
				<p class="hint">
					Drag to turn, scroll to zoom, right-drag to pan. Click a frame or a name to fly to it.
				</p>
			{/if}
		</div>
	</div>
</div>

<style>
	.library3d {
		display: grid;
		grid-template-rows: minmax(0, 1fr) auto;
		min-height: 0;
		position: relative;
	}
	.stage {
		min-height: 0;
		overflow: hidden;
	}
	.empty {
		position: absolute;
		top: 2rem;
		left: 1rem;
		right: 1rem;
		margin: 0;
		color: var(--map-muted);
	}
	.info {
		display: grid;
		gap: 0.35rem;
		padding: 0.6rem 1rem 0;
		border-top: 1px solid var(--map-line);
		font-size: 0.85rem;
	}
	.info p {
		margin: 0;
	}
	.top {
		display: flex;
		align-items: start;
		justify-content: space-between;
		gap: 0.5rem 1rem;
	}
	.summary,
	.context,
	.why,
	.hint,
	summary {
		color: var(--map-muted);
	}
	summary {
		cursor: pointer;
		font-size: 0.8rem;
		width: fit-content;
	}
	table {
		margin: 0.35rem 0 0.25rem;
		border-collapse: collapse;
		font-size: 0.8rem;
	}
	th,
	td {
		padding: 0.1rem 0.75rem 0.1rem 0;
		text-align: right;
		font-weight: normal;
	}
	th[scope='row'],
	thead th:first-child {
		text-align: left;
	}
	thead th {
		color: var(--map-muted);
	}
	/* One height, empty or full, so the graph above never resizes as it is clicked. */
	.details {
		display: grid;
		align-content: start;
		gap: 0.25rem;
		height: 4.6rem;
		overflow: hidden;
	}
	.what {
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
	.context {
		margin-left: 0.5rem;
		font-size: 0.8rem;
	}
	.why {
		font-size: 0.8rem;
		max-height: 1.35em;
		overflow: hidden;
	}
	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}
	.actions a,
	.actions button {
		font: inherit;
		font-size: 0.85rem;
		color: var(--map-ink);
		background: none;
		border: 1px solid var(--map-line);
		border-radius: 0.25rem;
		padding: 0.3rem 0.6rem;
		cursor: pointer;
		text-decoration: none;
	}
	.actions a:hover,
	.actions button:hover {
		border-color: var(--map-ink);
	}
	.actions button[aria-pressed='true'] {
		background: var(--map-raised);
		border-color: var(--map-ink);
	}
	@media (max-width: 40rem) {
		.info {
			padding: 0.5rem 0.75rem 0;
		}
		.details {
			height: 6rem;
		}
		.what {
			white-space: normal;
			max-height: 2.7em;
		}
	}
</style>
