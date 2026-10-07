# Content cleanups

Small content fixes landed by `skills/content-cleanup/SKILL.md`, one entry
each, newest last. Each is a mini-sprint (branch `cleanup-<tag>`, `just
check`, a squash-merged PR, both deploys) with no korg work item and no
numbered sprint record of its own.

## 2026-10-06 · cleanup-vietnam-blood-dist

**What:** `blood/vietnam-blood`'s map 5 (Whole Blood Supply and
Distribution System, July 1969) could not be read. The cited source,
archive.org's `CMHPub90-16` PDF, embeds the plate at only 408×653 and
heavily compressed, and `map-5.jpg` was that image enlarged to 1032×1290.
The scan was poor at the source, and nothing kloom did made it worse.

**Change:** In place of an upscale, we found a better source. The Army
Medical Department Office of Medical History's web edition published each
map as its own PDF. The Wayback Machine's 2004 capture of
`ch09map05.pdf` (1.4 MB) holds a lossless 924×1274 scan with every label
legible. Captures from 2010 on are a 74 KB recompressed copy. The scan's only
fault was text from the facing page (table 9) showing through the paper.
One levels curve over the whole image (input 70–150 stretched to 0–255)
whitened that and kept the line work. Nothing was drawn, sharpened or
upscaled. Saved as a grayscale JPEG. The media citation now points at the
2004 capture and its `note` records the levels pass. Because the source
changed, the frame carries a `revision` entry in `edits`.

**Repaired in passing:** the skill's own step 7, written before its first
run, deleted a local branch that `gh pr merge --delete-branch` had already
deleted. It now checks the merge's own cleanup instead.

### Deployed

2026-10-06 (2026-10-07 UTC) from `main` at `efe4c752` (PR #65). **The
service on kai:** `just deploy`, all ten `just verify` checks ok, library
`845acb`, content clone at the same commit; `/blood/vietnam-blood` and
`/media/blood/vietnam-blood/map-5.jpg` 200 on :4891, the map byte-identical
to the repo's. **The public site:** `just publish-public`, Fly release v19,
image `kloom-reader:efe4c752a-202610070512`, library `1466e1`, every
verify-public check ok.
