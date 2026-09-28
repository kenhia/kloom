import type { Citation } from '../model';

/**
 * Wikipedia links pinned to a revision (docs/design.md §Citations: articles
 * change, so a citation names the revision read). The TypeScript twin of
 * `create-tools/wiki-cite`, used when a kept answer carries pages a web turn
 * read. The revision pinned is the article's current one, which is the one
 * the model just read.
 */

const AGENT = 'kloom/0.1 (https://github.com/kenhia/kloom)';

/** Where a Wikipedia article URL points: its language site and title. Null otherwise. */
export function wikipediaArticle(url: string): { host: string; title: string } | null {
	let u: URL;
	try {
		u = new URL(url);
	} catch {
		return null;
	}
	if (!/^https?:$/.test(u.protocol) || !/^[a-z-]+(\.m)?\.wikipedia\.org$/.test(u.hostname))
		return null;
	const host = u.hostname.replace('.m.', '.');
	const path = /^\/wiki\/(.+)$/.exec(u.pathname)?.[1];
	const raw = path ?? (u.pathname === '/w/index.php' ? u.searchParams.get('title') : null);
	if (!raw) return null;
	return { host, title: decodeURIComponent(raw).replace(/_/g, ' ') };
}

const quote = (title: string) =>
	encodeURIComponent(title.replace(/ /g, '_')).replace(/%2C/g, ',').replace(/%27/g, "'");

export type Fetch = (url: string, init?: RequestInit) => Promise<Response>;

/**
 * A `wikipedia` citation for an article URL, pinned to the article's current
 * revision and dated by it. Throws when the article is missing or the lookup
 * fails: a Wikipedia page is never kept unpinned.
 */
export async function pinWikipedia(
	url: string,
	accessed: string,
	fetcher: Fetch = fetch
): Promise<Citation> {
	const article = wikipediaArticle(url);
	if (!article) throw new Error(`not a Wikipedia article: ${url}`);
	const query = new URLSearchParams({
		action: 'query',
		prop: 'revisions',
		rvprop: 'ids|timestamp',
		redirects: '1',
		format: 'json',
		titles: article.title
	});
	const res = await fetcher(`https://${article.host}/w/api.php?${query}`, {
		headers: { 'user-agent': AGENT },
		signal: AbortSignal.timeout(15_000)
	});
	if (!res.ok) throw new Error(`Wikipedia answered ${res.status} for "${article.title}"`);
	const data = (await res.json()) as {
		query?: {
			pages?: Record<
				string,
				{ title: string; missing?: string; revisions?: { revid: number; timestamp: string }[] }
			>;
		};
	};
	const page = Object.values(data.query?.pages ?? {})[0];
	const rev = page?.revisions?.[0];
	if (!page || 'missing' in page || !rev)
		throw new Error(`no Wikipedia article "${article.title}"`);
	return {
		kind: 'wikipedia',
		title: page.title,
		url: `https://${article.host}/w/index.php?title=${quote(page.title)}&oldid=${rev.revid}`,
		accessed,
		authors: [{ name: 'Wikipedia contributors' }],
		container: 'Wikipedia, The Free Encyclopedia',
		publisher: 'Wikimedia Foundation',
		published: rev.timestamp.slice(0, 10)
	};
}
