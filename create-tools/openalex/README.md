# openalex

OpenAlex lookups with the homelab's API key: whether a paper has an open
copy and where, its abstract, and its metadata. For authors with a shell
(author-subject sprints); grow jobs have no shell and don't use it.

```sh
python3 create-tools/openalex/openalex.py work 10.1038/171737a0
python3 create-tools/openalex/openalex.py work https://doi.org/10.1038/171737a0 --json
python3 create-tools/openalex/openalex.py search "Lister antiseptic principle" --per-page 5
python3 create-tools/openalex/openalex.py raw "works?filter=doi:10.1038/171737a0"
```

- `work` takes a DOI (bare, `doi:`, or a doi.org URL) or an OpenAlex work
  id (`W…`, or its openalex.org URL). It prints the title, year, venue,
  DOI, authors, the open-access status and `oa_url`, every open location
  (with its version: submitted, accepted or published), and the abstract,
  rebuilt from OpenAlex's inverted index.
- `search` lists matching works with the same facts. `--json` prints the
  raw records instead.
- `raw` prints the JSON for any API path.

**The key.** `OPENALEX_API_KEY`, from the environment or else from
`/etc/khomelab/secrets.env`, the host's one copy (k-homelab secret
`openalex-api-key`, krot `registry/openalex.toml`; ken reads it through the
`khomelab` group). Never copy it into a `.env` or a script. The tool adds
the key to each request and **never prints it**: output, errors and any URL
it reports are redacted, so it can't leak into a transcript the way a
`curl` command line with the key in it would. Without a key the tool still
runs, on OpenAlex's shared anonymous budget, and says so on stderr.

A rate limit (429) is waited out a few times, honouring `Retry-After`.
Standard library only; `test_openalex.py` runs under `just tools-test`
with no network.
