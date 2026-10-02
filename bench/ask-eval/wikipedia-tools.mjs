// The RA's web for the ask eval (korg 3483): two tools over English Wikipedia,
// in the OpenAI tool-calling format vLLM serves. The RA has no search of its
// own, so this shim stands in for Sonnet's WebSearch and WebFetch; it is
// narrower than they are, and the sprint record says so. Read-only: the
// worst a page can do is mislead the answer, as with ask's own web tools.

const API = 'https://en.wikipedia.org/w/api.php';
const UA = 'kloom-ask-eval (https://github.com/kenhia/kloom)';
/** How much of a page the model gets; a long article is cut, and says so. */
const PAGE_CHARS = 15_000;

export const TOOLS = [
	{
		type: 'function',
		function: {
			name: 'search',
			description:
				'Search English Wikipedia. Returns up to five articles, each with its title, URL and a snippet. This is the only search available.',
			parameters: {
				type: 'object',
				properties: { query: { type: 'string', description: 'What to search for.' } },
				required: ['query']
			}
		}
	},
	{
		type: 'function',
		function: {
			name: 'fetch',
			description:
				'Read an English Wikipedia article as plain text, given its URL (https://en.wikipedia.org/wiki/...). Other sites cannot be read.',
			parameters: {
				type: 'object',
				properties: { url: { type: 'string', description: 'The article URL.' } },
				required: ['url']
			}
		}
	}
];

const api = async (params) => {
	const url = `${API}?${new URLSearchParams({ format: 'json', formatversion: '2', ...params })}`;
	const res = await fetch(url, {
		headers: { 'user-agent': UA },
		signal: AbortSignal.timeout(20_000)
	});
	if (!res.ok) throw new Error(`Wikipedia answered ${res.status}`);
	return res.json();
};

const articleUrl = (title) =>
	`https://en.wikipedia.org/wiki/${encodeURIComponent(title.replaceAll(' ', '_'))}`;

const unhtml = (s) =>
	s
		.replace(/<[^>]+>/g, '')
		.replace(/&quot;/g, '"')
		.replace(/&#0?39;/g, "'")
		.replace(/&amp;/g, '&');

export async function search(query) {
	const j = await api({ action: 'query', list: 'search', srsearch: query, srlimit: '5' });
	const hits = j.query?.search ?? [];
	if (!hits.length) return `No Wikipedia articles found for "${query}".`;
	return hits.map((h) => `${h.title} — ${articleUrl(h.title)}\n${unhtml(h.snippet)}`).join('\n\n');
}

/** The article a Wikipedia URL names, or null for any other URL. */
export function wikipediaTitle(url) {
	let u;
	try {
		u = new URL(url);
	} catch {
		return null;
	}
	if (!/^(en\.)?(m\.)?wikipedia\.org$/.test(u.hostname.replace(/^www\./, ''))) return null;
	const m = u.pathname.match(/^\/wiki\/(.+)$/);
	return m ? decodeURIComponent(m[1]).replaceAll('_', ' ') : null;
}

export async function read(url) {
	const title = wikipediaTitle(url);
	if (!title)
		return 'Only English Wikipedia articles (https://en.wikipedia.org/wiki/...) can be read.';
	const j = await api({
		action: 'query',
		prop: 'extracts',
		explaintext: '1',
		redirects: '1',
		titles: title
	});
	const page = j.query?.pages?.[0];
	if (!page || page.missing || !page.extract) return `There is no Wikipedia article "${title}".`;
	const text = page.extract;
	const head = `${page.title} — ${articleUrl(page.title)}\n\n`;
	return text.length > PAGE_CHARS
		? `${head}${text.slice(0, PAGE_CHARS)}\n\n[The article continues; only the first ${PAGE_CHARS} characters are shown.]`
		: head + text;
}

/** Run one tool call; a failure is reported to the model as text, never thrown. */
export async function runTool(name, rawArgs) {
	let args;
	try {
		args = JSON.parse(rawArgs || '{}');
	} catch {
		return `The arguments were not valid JSON: ${rawArgs}`;
	}
	try {
		if (name === 'search') return await search(String(args.query ?? ''));
		if (name === 'fetch') return await read(String(args.url ?? ''));
		return `There is no tool called "${name}".`;
	} catch (e) {
		return `The tool failed: ${e.message}`;
	}
}
