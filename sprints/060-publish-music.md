# 060 — Publish Sound and Score

Ken approved publishing Sound and Score on the public reader site
(korg:4927, covering korg:4926). The subject was in the repo and absent
from the public manifest. The branch started from clean, current `main`
at `9329434b`, with no pending grown content.

Added `music` between `biology` and `datacenters` in `publish.json` to
preserve subject creation order. The public compiler uses the manifest
to select subjects. The database lists them by subject ID, and the
start screen uses that order for both the desktop list and the mobile
picker. The root URL uses the configured default subject, falling back
to the first subject by ID if that default is absent. Linked sprint
058's publishing decision to this record.

`just stage-public` staged 14 subjects and 2,054 media files. A query of
`build-public/content.db` found 67 music frames, including 17 across
three trails (piano 6, tuning 6, voice 5). All 149 music media files
were copied (75 JPEGs and 74 SVGs).

The reader uses the shared Chicago formatter for citations, including
`recording`. The staged music media are images, and listening to cited
recordings depends on the linked source. Audio playback in kloom is
outside this sprint.

## Repaired in passing

- Fixed the Markdown formatting in sprint 059's deployment checklist
  after Prettier flagged it in `just check`.
