---
name: kloom-review-notes
description: Find the notes and annotations kloom readers flagged for "Agent review" (on kai's service, a dev server, or the public reader site), deal with each one (usually a fix to the frame it is on), and mark it handled with what was done; and list the subjects readers suggested, promote one to korg and mark its status. Use when Ken asks to review flagged notes, "look at my kloom notes", "what subjects have readers suggested", or run the review-notes skill.
---

# Reviewing flagged notes

While reading a kloom subject, a reader can write a **note** on a frame and
tick **Agent review**. It flags the note for an agent to deal with later:
wording that confused them, a date that looks wrong, a question the frame
should answer. An **annotation** is a note on some words of the frame's
narrative, the ones the reader selected: it points at the exact wording. This
skill finds every flagged note and annotation, and for each one records what
was done. The reader sees your answer under their note, in the frame's
Notes tab.

Notes are reader data (`docs/design.md` §Reader data, §Notes, §Annotations). They live in
the reader store (`<data>/reader.db`), not in git, and one belongs to one
reader. Reach them through `review-notes.mjs` beside this file, which opens
the store through its adapter. **Never open `reader.db` with `sqlite3` or
any other tool**: the adapter is the only way in (`CLAUDE.md`).

## Where the notes are

Run the script from the kloom checkout with Node 24 or later. Say where
the notes are first:

- **the public reader site**, kloom.kenhiatt.us: `--public`. The script
  runs `admin.mjs` on the Fly machine through `fly ssh console`
  (`deploy/fly.sh`, so only on kai), reading and writing the live store.
  It never pushes a database back, and never needs `just pull-notes`
  first.
- **the service on kai** (where Ken reads):
  `--data ~/.local/share/kloom/data`
- the dev server: `./data`, the default

```sh
node skills/review-notes/review-notes.mjs --public list
node skills/review-notes/review-notes.mjs --data ~/.local/share/kloom/data list
```

Review each place that has readers. A note belongs to the store it is in:
answer it there.

`list` prints each flagged note, oldest first. Each entry shows the reader
(their display name and login, on the public site), the note id, the frame
(`subject/frame`, and its title as the reader saw it), the frame's content
directory, when it was written, the `--seen` value to answer it with, and
the note's text. An annotation is marked `(annotation)` and quotes the
words it is on (`> …`), whitespace collapsed, as they read in the
narrative, so look for them in `reading.md` across line breaks. Add
`--reader <login>` to see one reader's notes only, or `--json` for the
records.

## For each note

1. **Read the frame first.** Read `frame.json` and `reading.md` in the
   content directory the entry names, and the frames on either side if the
   note is about sequence. On kai the service reads its own content clone,
   `~/.local/share/kloom/content`. Make changes in this repo, never in that
   clone.
2. **Decide what the note asks for.** For an annotation, it is about the
   quoted words first: start there.
   - **A fix you can make:** wording, a wrong date, a missing step, a broken
     citation. Make it the way the grow skill says content is written
     (`skills/grow/SKILL.md`): the same voice, Chicago-style citations, at
     least one key citation, Wikipedia by `oldid`. Then run `just check`.
     A content change ships like any other: on a branch, through a PR.
   - **A question:** answer it in the response. If the frame should answer
     it too, that is a fix.
   - **Something that needs Ken:** a design question, or a new frame or
     trail. File it in korg (project `kloom`) and name the item in the
     response.
   - **Nothing to do:** say why in the response. Handling a note is not the
     same as agreeing with it.
3. **Mark it handled**, with one or two sentences the reader will read under
   their note:

   ```sh
   node skills/review-notes/review-notes.mjs --public \
     handle <login> <note-id> "Reworded the second paragraph; the ember was in a fennel stalk, not a reed." \
     --seen <updated>
   ```

   With the same target as the `list`, and `--seen` the value it printed.
   The answer is refused if the reader has deleted the note, unflagged it,
   or edited it since you listed it: list again and read what they wrote
   now. With several answers ready, put them in a JSON file, a list of
   `{"reader", "id", "response", "seen"}`, and send them in one call:
   `handle --file results.json`. A refusal names the note and why; the
   others still land.

   Say what you changed and where, or what you filed, or why nothing
   changed. If you reworded an annotation's quoted words, it can no longer
   find them and shows as detached (with the words it quoted): say in the
   response what they became. Handle a note once the fix is committed (or the item filed), not
   before: the reader takes "handled" to mean it is done.

A handled note stays in the reader's list with your response. Handling it
also counts it as a new answer on their My notes control until they have
seen it, and My notes lists it as Answered, where they can clear it. If they
tick Agent review again (in the editor, or "Ask the agent again" in My
notes), it comes back flagged, and your old response is cleared.

## Suggested subjects

Readers can suggest a subject from the start screen's About panel (korg
3459): a title, what it should cover, and why they would like it. Each is a
note to Ken, never a job: nothing runs from one. They are in the same store
as the notes, and the same targets reach them:

```sh
node skills/review-notes/review-notes.mjs --public suggestions [--status new] [--json]
node skills/review-notes/review-notes.mjs --public mark-suggestion <login> <id> planned
```

A status is `new` (the reader sees "Sent"), `planned`, `written` or
`declined`, and the reader sees it beside their suggestion. Only this side
changes it.

- **To promote one**, file a korg work item in project `kloom` titled
  `Future subject: <title>`, like the others already filed (search korg for
  "Future subject" first: if one exists, comment on it instead). Say who
  suggested it by display name, and quote what they asked it to cover. Then
  mark the suggestion `planned` and tell Ken the item's number.
- `written` is for when the subject ships; `declined` needs Ken's say.
  Don't decline one on your own judgement: list it for Ken.

## Rules

- Never change a note's text: it is the reader's. The response is yours.
- A note may be about something the frame does not say. Check before you
  "fix" a frame to agree with a note.
- The notes are personal. Quote them in a commit message or a korg item only
  as far as the fix needs.
