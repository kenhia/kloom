---
name: kloom-content-cleanup
description: Land a small content fix in kloom (a blurry image swapped for a legible scan, a wrong date, a broken citation, a caption) as a mini-sprint with no korg work item and no numbered sprint record. Checks the repo is on a clean main, branches `cleanup-<tag>`, makes the change, logs it in `sprints/content-cleanup.md`, runs `just check`, then commit, PR, squash merge, clean up locally, `just deploy` and `just publish-public`. Use when Ken asks for a "simple update", a "cleanup", or a one-frame fix he wants live now.
---

# Content cleanup

A numbered sprint (`sprints/###-<name>.md`, a korg proposal, work items) is
the right size for a feature. It is too much ceremony for one frame's fix.
A cleanup is a mini-sprint: the same gate, PR and deploys, with a dated
entry in one running log, `sprints/content-cleanup.md`, instead of a record
of its own.

## Is it a cleanup?

Yes, when **all** of these hold:

- It changes content only: files under `subjects/` or `names/` (a reading,
  a `frame.json`, an image or chart, a name). No `engine/`, `src/`,
  `create-tools/`, `deploy/` or `justfile` change.
- It is a few frames at most, and no frame is added or removed. New frames
  are grow (`skills/grow`) or authoring (`skills/author-subject`).
- Nothing in it needs a decision from Ken that he has not already made in
  the conversation.

Otherwise, file a korg work item and run a sprint. If it was a cleanup
until a code change turned up, stop and say so; don't widen the branch.

## 1. Preflight

```sh
git fetch origin
git branch --show-current            # main
git status --porcelain               # nothing
git rev-parse HEAD origin/main       # the same commit
just grow-pending                    # exit 0
```

Any of the first three wrong: stop and tell Ken (the `resolve-repo-state`
skill walks the options). Never stash or reset his work to get through.
`just grow-pending` exiting 1 means grown content waits for review. That
review ships as its own PR first (CLAUDE.md), so tell Ken and let him
choose between running `skills/review-grown` now and going ahead with the
cleanup.

## 2. Branch

```sh
git checkout -b cleanup-<short-tag>
```

The tag names the thing fixed, in a few words: `cleanup-vietnam-blood-dist`
for the distribution map in `blood/vietnam-blood`.

## 3. Make the change

All of CLAUDE.md's content rules apply, and three of them come up in
nearly every cleanup:

- **`edits`.** A changed fact, date, attribution, quotation or source on a
  published frame gets an `edits` entry in its `frame.json`, newest first
  (`skills/grow/SKILL.md` §Edits and corrections). A new scan of the same
  image is a changed source, so it gets one. A typo does not.
- **Media citations.** A replaced image keeps a `media` citation with a
  `licence`. Point `url` at where the new file really came from, and put
  anything done to it in `note` ("Levels adjusted to remove show-through").
- **American English** in kloom's own words; `just check` flags the rest.

Images:

- Look for a better **source** before you try to improve a file. A blurry
  plate is usually a small copy of a good scan. Try the publisher's own
  web edition (live, or on the Wayback Machine, where an older capture can
  be the uncompressed one), then the book's other scans.
- What you may do to a found scan: crop, rotate, a levels or contrast
  curve, grayscale, resizing **down**. Each one is recorded in the
  citation's `note`.
- Upscaling or AI enhancement makes up detail, and on a map or chart that
  detail can be wrong. Don't use it unless Ken has agreed to it in the
  conversation. If he has, the caption must say the image was enhanced from
  a low-resolution source and may contain errors.
- Work in `.scratch/cleanup-<short-tag>/`, not `/tmp`. Write commit
  messages and PR bodies to files there too (`git commit -F`,
  `gh pr create --body-file`): text sent through `ssh '…'` breaks on its
  first apostrophe. When you replace an
  image, write the new file and `mv` it over the old one. Some media files
  are hard-linked into `.scratch` copies, and writing into them in place
  changes those copies too.

## 4. Log it

Add an entry at the end of `sprints/content-cleanup.md`, newest last:

```markdown
## YYYY-MM-DD · cleanup-<short-tag>

**What:** the frame(s) and what was wrong, in a sentence or two.

**Change:** what you did and where the fix came from (the source, with its
URL; what was done to an image).

**Repaired in passing:** (only if there was any)
```

The `### Deployed` part is added in step 8, after the deploys, never
written ahead of them.

## 5. Gate

```sh
just check
```

It must pass in full. Any other check whose surface you touched runs too.
A change to a frame's scene (`frame.json` `scene`, `scene.svg`) runs
`just scene-fit <subject>`.

## 6. Commit, PR, merge

```sh
git add -A subjects names sprints/content-cleanup.md
git commit        # fix(cleanup): <what>  (a body that says why; Co-Authored-By trailer)
git push -u origin cleanup-<short-tag>
gh pr create --fill
gh pr merge --squash --delete-branch
```

The title is `fix(cleanup): …` for something that was wrong, or
`content(cleanup): …` for an improvement. The squash merge is what the
Changelog and the frames' `added` dates read (`engine/history.ts`), so
always squash. kloom has no GitHub CI: `just check` in step 5 is the gate.

## 7. Clean up locally

`gh pr merge --delete-branch` does most of it: it deletes the remote
branch, checks out `main`, fast-forwards it and deletes the local branch.
Confirm that it did:

```sh
git branch --show-current             # main
git rev-parse HEAD origin/main        # the same commit: the squash merge
git branch --list 'cleanup-*'         # nothing
git status --porcelain                # nothing
```

If the merge was made another way (the GitHub UI), do it by hand:
`git checkout main && git pull --ff-only && git branch -D cleanup-<short-tag>`
(`-D`, because a squash merge is not an ancestor).

## 8. Deploy, then record it

Run these on kai, from the merged `main` (docs/deploying.md):

```sh
just deploy           # the service on kai; ends with `just verify`
just publish-public   # kloom.kenhiatt.us; ends with verify-public
```

`just deploy` restarts the service, which takes merged `main` into its
content clone and rebuilds the library. Check the fixed frame live on the
ssh door, `http://127.0.0.1:4891/<subject>/<frame>` and any media you
changed under `/media/<subject>/…`. Each must answer 200.

`publish-public` only ships subjects in `publish.json`. If the cleanup's
subject is not in it, skip the publish and say so in the log.

Then add the deploy to the entry and push it straight to `main`, as every
sprint's deploy record goes:

```markdown
### Deployed

YYYY-MM-DD from `main` at `<short sha>` (PR #N): the service on kai (`just
verify` all ok, the frame and its media 200 on :4891) and the public site
(Fly release vNN, image `kloom-reader:<label>`, verify-public all ok).
```

```sh
git commit -am "docs(cleanup): record the deploy of cleanup-<short-tag> [skip ci]"
git push
```

## 9. Report

Tell Ken what was fixed, the PR, and that both deploys verified. Give the
fixed frame's public URL. Paths and hashes stay in the log.
