---
name: kloom-review-grown
description: Review content a kloom grow job wrote (on the service's grow/kai, a dev server's grow/dev-<host>, or an older grow-* branch) before it reaches main. Check the facts against the sources, repair what can be repaired, flag what can't, and merge it through a PR whose squash carries the Grow-reviewed trailer. Use when `just grow-pending` exits 1 (every sprint checks first, CLAUDE.md), or when Ken asks to review grown content.
---

# Reviewing grown content

A grow job writes frames, trails, names and connections into a subject
(`skills/grow/SKILL.md`). It works with a model that has web search but no
shell, and the job commits only what passes `validate()` (the commit says
`Validated: yes`). That is necessary, not sufficient. **Grown content
reaches `main` only through this review** (Ken, 2026-10-02, korg 3442),
because `main` is what the public reader site publishes. You have what the
grow job did not: a shell, the validator, `create-tools/`, and the web.

## Where grown content waits

- **The service's branch, `grow/kai`.** The service on kai grows into its
  own content clone (`~/.local/share/kloom/content`) and pushes this branch.
  Review `origin/grow/kai`; never edit that clone.
- **A dev server's branch, `grow/dev-<host>`.** A dev server grows into a
  worktree of the checkout (under `~/.cache/kloom/`, or
  `$KLOOM_GROW_WORKTREE`) on this branch, and pushes it. Review the local
  branch, or `origin/grow/dev-<host>` from another host.
- **Older branches, `grow-*`.** These are from before the grow branches had
  their names. Most are merged already.

```sh
just grow-pending        # fetches; lists every grow branch; exits 1 if any is PENDING
```

A branch is **merged** when `main` has all its content: its commits are in
`main`'s history, or some commit on `main` holds every path they touched as
they left them (a squash merge, even one edited since), or a review merged
it and said so in a `Grow-reviewed` trailer. Anything else is **PENDING**,
and is what you review.

## For each pending branch

1. **Take only what is new, on top of `main`.** Branch from `origin/main`
   and cherry-pick the grow commits `main` does not have yet. They keep their
   author, message and `Validated: yes`.

   ```sh
   git fetch origin
   git checkout -b review-grown/<branch-name>-<YYYYMMDD> origin/main
   git log --oneline origin/main..<ref>      # the pending commits; `git cherry` agrees
   git cherry-pick <first>^..<ref>           # or one by one, skipping any already merged
   ```

   A commit `main` already has (an earlier review merged it) cherry-picks
   empty. Skip it with `git cherry-pick --skip`. Note the tip you reviewed:
   `git rev-parse <ref>`. The trailer names it.

2. **Check it is correct.** "Correct" for grown content has five parts:
   - **It validates.** `just check`. The job already ran the validator, but
     `main` may have moved since, and the validator does not check
     spelling: a British spelling `just check` flags in the grown frames is
     a wording repair (`python3 create-tools/spelling/american.py apply
<the frames>`), with no `edits` entry.
   - **The fact rule:** every claim against the source it rests on, read
     where the grow job could not.
     - Open each key citation, and the citations that carry a reading's
       particular claims (a date, a figure, a quotation).
     - The job had no shell. Read PDFs with `create-tools/read-source`, find
       papers with `create-tools/openalex`, and use the routes in
       `skills/grow/reaching-sources.md` for pages that refuse a script.
     - A claim that matches its source passes. A quotation must match word
       for word.
     - Repair or cut a claim the source does not support. Never leave a
       claim standing on a source you could not read: mark the citation
       `read: "abstract"`, `"excerpt"` and so on, as §Sources and citations
       says.
   - **Names and connections:**
     - **Names:** each name the job added to `names/` must hold the right
       Wikidata item. Check it with
       `python3 create-tools/names/names.py lookup "<Wikipedia title>" --expect <word>`.
       The job could not check the ID, only its form. A wrong item is
       either corrected or set to `null`.
     - **Connections:** each connection's `why` must be true against the
       other frame's reading, which you read in full.
   - **House style:** the voice and the scene rules in
     `skills/grow/SKILL.md`. The plate must draw what the reading says;
     render it and look (`create-tools/draw-plates/contact_sheet.py`).
     Citations must resolve, with `read`, `citedIn` and `mirror` used as
     §Sources and citations says.
   - **An accurate commit message.** If the job's summary says something
     untrue ("not validated", "read in full" for an abstract), say so in
     your repair commit. History isn't rewritten.

3. **Repair what you can, as commits of your own** on the review branch.
   Each says what it fixes (`review-grown(nursing): navy-pow — Olds, not
Jackson, for the barracks`). A repair follows the same rules as any
   content: `just check`, a key citation, Wikipedia by `oldid`. A repair to
   a grown frame's facts (a claim, date, attribution, quotation or source
   changed or cut) adds an entry to its `edits`, as `skills/grow/SKILL.md`
   §Edits and corrections says: the frame may already have been read on
   the service, where it showed as soon as it was grown. A repair of
   wording alone does not.

4. **Flag what you can't repair.** That is a claim you could not check
   (the source is unreachable from here), or a choice that is Ken's (a frame
   that should not be in the subject at all). Prefer cutting a claim you
   could not check to leaving it. If what is left of a frame does not stand
   on its own, take the frame out, and its spine entry, and say so.

5. **Open the PR.** Push the review branch and open it against `main`:
   - **Title:** `review-grown: <subject> — <frames added>`.
   - **Body:**
     - **What the grow added:** frames, trails, names, connections.
     - **Checked:** each claim or citation you checked, against what.
     - **Repaired:** what, and why.
     - **Flagged:** what, and why.
     - **Reviewed:** the branch and tip sha.

6. **Merge it** when `just check` passes and nothing flagged is a claim you
   believe is false. That's the default, under agent-skills korg:3422's
   rule. **Squash**, and end the squash message with the trailer, as its own
   last paragraph, one line per branch tip reviewed:

   ```sh
   gh pr merge <n> --squash --subject "review-grown: <subject> — <frames>" \
     --body "$(printf '%s\n\nGrow-reviewed: %s (%s)' "<two lines: what came in, what was repaired>" "<full tip sha>" "<ref>")"
   ```

   The trailer is what tells kloom the branch is done, even though `main`
   now holds the repaired version rather than the job's. `just grow-pending`
   then reads it as merged. The service's clone resets `grow/kai` to `main`
   at its next start (a deploy is one), instead of trying to rebase what you
   repaired. A dev worktree moves to `main` before its next grow. Without
   the trailer a repaired merge reads as pending forever.

   **Leave it open, and ask Ken** (korg, Awaiting Ken), when a flag is his
   call: a frame you would cut whole, or a source dispute you can't settle.

7. **Confirm.** Pull `main`, and run `just grow-pending`: nothing pending.

## Rules

- **Never push to a grow branch** (`grow/kai`, `grow/dev-*`). It belongs to
  the server that grows on it. Your work goes on the review branch. The
  trailer is how the grow branch learns it was merged.
- **Never edit the service's content clone** on kai. It syncs from `main`.
- Review **before** the sprint's own work, and ship it as its own PR
  (CLAUDE.md). A review is not folded into a feature sprint's commit.
- The `Validated: yes` trailer says the job ran `validate()`. It says
  nothing about the facts. That is this review.
