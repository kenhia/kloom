# commons-media

Images from Wikimedia Commons for a reading, with the `media` citation the
validator requires (sprint 006, written for the ai subject).

```sh
python3 create-tools/commons-media/commons_media.py search "Mark I Perceptron"
python3 create-tools/commons-media/commons_media.py fetch "File:Name.jpg" subjects/<subject>/frames/<frame> --as short-name [--width 960]
python3 create-tools/commons-media/commons_media.py fetch "File:Book.pdf" subjects/<subject>/frames/<frame> --page 12
uv run create-tools/commons-media/commons_media.py fetch "File:Engraving.png" subjects/<subject>/frames/<frame> --jpeg
uv run create-tools/commons-media/commons_media.py jpeg .scratch/page.png subjects/<subject>/frames/<frame>/page.jpg
```

- `search` lists image files (not PDFs or video) matching the text, each
  marked `ok` when its licence is public domain, CC0 or CC BY(-SA), with its
  size and author.
- `fetch` refuses any other licence. It downloads a scaled copy into the
  frame directory as `<short-name>.<ext>`. Commons serves thumbnails only at
  fixed widths (120, 250, 330, 500, 960, 1280, 1920) and rounds a request
  up, so `--width` (default 960) takes the widest step no wider than
  asked. It warns when the file is over 350 KB; try `--width 500`.
- It prints the citation from the file page's own metadata, and on stderr
  what to check in it (sprint 027, from 13 of sprint 025's authors
  rewriting every citation by hand):
  - **the licence tags** the file page carries (`PD-Art, PD-US-expired,
PD-old-100`), since "Public domain" hides which: `PD-Art` covers only
    a faithful photograph of a flat work, and a `PD-USGov` tag can sit on
    a photograph no government employee took;
  - **no `container`**: it used to write "Via Wikimedia Commons", which
    every author replaced with where the work is from (a museum, a book).
    Add that from the file page;
  - **authors** as family and given names when the Artist field is a
    plain personal name (life dates dropped), otherwise as a `name`, and
    none at all for boilerplate: an unknown author in any template
    ("AnonymousUnknown author", 不明, unbekannt), "Own work", or a
    scanner's make. It says when it left the author out, and when it
    wrote a `name` you may need to split;
  - **the date**, with `circa` for "c." or "circa", and a date BC as
    `"1504 BC"`, the form `published` takes since sprint 027 (sprint 026
    found "c. 1504 BC" written as AD 1504).
- **`--page N`** takes one page of a PDF or DjVu on Commons as a JPEG (a
  scanned book's plate), named `<short-name>-pN.jpg`, and cites the file
  page with `?page=N`.
- **`--jpeg`** converts what it fetched to JPEG, and the **`jpeg`**
  command converts a page you cropped yourself; both composite a PNG's
  transparency onto white first (sprint 026's Frere engraving turned
  black). They need Pillow, which `uv run` installs from the script's
  inline metadata (korg 3404); everything else is standard library and
  runs with `python3`.
- Anything but public domain or CC0 gets a caption credit, which the page
  builds from the `media` citation (docs/design.md §Citations). Write no
  credit or caption line under the image yourself.
- `test_commons_media.py` is its test (`just check` runs it; no network).

Commons metadata is what uploaders typed. Open the file page and look at the
image before you use it: the licence is stated there, and a file's name does
not always say what it shows.
