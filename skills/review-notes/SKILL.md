---
name: kloom-review-notes
description: Find the notes and annotations kloom readers flagged for "Agent review", deal with each one (usually a fix to the frame it is on), and mark it handled with what was done. Use when Ken asks to review flagged notes, "look at my kloom notes", or run the review-notes skill.
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

Run the script from the kloom checkout with Node 24 or later. `--data`
names the app's data directory:

- **the service on kai** (where readers actually read):
  `--data ~/.local/share/kloom/data`
- the dev server: `./data`, the default

```sh
node skills/review-notes/review-notes.mjs --data ~/.local/share/kloom/data list
```

`list` prints each flagged note, oldest first. Each entry shows the reader,
the note id, the frame (`subject/frame`, and its title as the reader saw
it), the frame's content directory, and the note's text. An annotation is
marked `(annotation)` and quotes the words it is on (`> …`), whitespace
collapsed, as they read in the narrative, so look for them in `reading.md`
across line breaks. Add
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
   node skills/review-notes/review-notes.mjs --data ~/.local/share/kloom/data \
     handle <login> <note-id> "Reworded the second paragraph; the ember was in a fennel stalk, not a reed."
   ```

   Say what you changed and where, or what you filed, or why nothing
   changed. If you reworded an annotation's quoted words, it can no longer
   find them and shows as detached (with the words it quoted): say in the
   response what they became. Handle a note once the fix is committed (or the item filed), not
   before: the reader takes "handled" to mean it is done.

A handled note stays in the reader's list with your response. If they tick
Agent review again after editing it, it comes back flagged, and your old
response is cleared.

## Rules

- Never change a note's text: it is the reader's. The response is yours.
- A note may be about something the frame does not say. Check before you
  "fix" a frame to agree with a note.
- The notes are personal. Quote them in a commit message or a korg item only
  as far as the fix needs.
