# commons-media

Images from Wikimedia Commons for a reading, with the `media` citation the
validator requires (sprint 006, written for the ai subject).

```sh
python3 create-tools/commons-media/commons_media.py search "Mark I Perceptron"
python3 create-tools/commons-media/commons_media.py fetch "File:Name.jpg" subjects/<subject>/frames/<frame> --as short-name [--width 960]
python3 create-tools/commons-media/commons_media.py fetch "File:Book.pdf" subjects/<subject>/frames/<frame> --page 12
python3 create-tools/commons-media/commons_media.py fetch "File:Engraving.png" subjects/<subject>/frames/<frame> --jpeg
python3 create-tools/commons-media/commons_media.py jpeg .scratch/page.png subjects/<subject>/frames/<frame>/page.jpg
python3 create-tools/commons-media/commons_media.py crop .scratch/scan.png subjects/<subject>/frames/<frame>/page.jpg --box 120,80,1480,2100
```

- `search` lists image files (not PDFs or video) matching the text, each
  marked `ok` when its licence is public domain, CC0 or CC BY(-SA), with its
  size and author.
- `fetch` refuses any other licence. It downloads a scaled copy into the
  frame directory as `<short-name>.<ext>`. Commons serves thumbnails only at
  fixed widths (120, 250, 330, 500, 960, 1280, 1920) and rounds a request
  up, so `--width` (default 960) takes the widest step no wider than
  asked. It warns when the file is over 350 KB; try `--width 500`. A
  kilobyte is a thousand bytes (sprint 057: it counted 1,024, so a
  357,354-byte file passed as "348 KB"). A `--width` wider than the
  original is refused, with the original's width; leave `--width` out to
  take an original narrower than 960.
- **A page with two licences** (sprint 057, korg 3576): a photograph of an
  old artwork carries the artwork's public-domain tag and the photograph's
  Creative Commons licence (`{{Art Photo}}`'s `photo license`,
  `{{Licensed-PD-Art|PD-old-100|cc-by-sa-4.0}}`, or `{{self|cc-by-sa-4.0}}`
  beside `{{PD-old-100}}`), and a scan can carry Commons' PD tag beside its
  source's CC BY (the Biodiversity Heritage Library's Flickr scans).
  Commons' summary says "Public domain", and `fetch` used to write that. It
  now writes the Creative Commons licence, the more restrictive, and warns
  naming both. The author is then the photographer when the page names one
  (`{{Art Photo}}`'s `photographer`, a `[[User:…]]` source, or the uploader
  of an own work), with the artwork's author said on stderr.
- **What it warns of in the author and the title** (sprint 057, korg 3576
  and 3557), none of them refused: several people written as one name
  ("Jawahar Swaminathan and MSD staff at …", a figure's eight authors
  between commas); a title that is the file's name (a journal figure's
  `Microorganisms-09-01822-g001`, with the credit line's "Fig. 1 at …"
  when it has one); a plate or figure from a book, whose Artist may be the
  book's author rather than the plate's artist, and whose plate number on
  Commons may be wrong; an engraving or printing firm ("Cole, Swain &
  Sons", "Day & Son, Lithrs."), which is `engravers`; a library catalog's
  heading ("Villard, de Honnecourt, active 13th century."); and a
  collection ("Miscellaneous Items in High Demand, PPOC, Library of
  Congress"). A firm (Sons, Bros, Brothers) is a `name`, never family and
  given. Fetched anywhere but a frame's directory, it says that `file`
  names the fetched copy, to be set to the cropped file's name.
- **Flickr's "No restrictions"** (the Internet Archive's book scans, the
  Smithsonian's photographs) is not a licence but a statement that none is
  known. `fetch` takes it as public domain, with a warning and an empty
  `note`, which the gate refuses until you write the public-domain basis
  in it ("Published in the US in 1890"), from the work itself, not the
  Flickr page (sprint 029). The Internet Archive Book Images account is
  not written as the author.
- It prints the citation from the file page's own metadata, and on stderr
  what to check in it (sprint 027, from 13 of sprint 025's authors
  rewriting every citation by hand):
  - **the licence tags** the file page carries (`PD-Art, PD-US-expired,
PD-old-100`), since "Public domain" hides which: `PD-Art` covers only
    a faithful photograph of a flat work, and a `PD-USGov` tag can sit on
    a photograph no government employee took;
  - **no `container`**, except for the three institutions below: it used
    to write "Via Wikimedia Commons", which every author replaced with
    where the work is from (a museum, a book). Add that from the file page;
  - **authors** as family and given names when the Artist field is a
    plain personal name (life dates dropped), otherwise as a `name`, and
    none at all for boilerplate: an unknown author in any template
    ("AnonymousUnknown author", 不明, unbekannt), "Own work", or a
    scanner's make. It says when it left the author out, and when it
    wrote a `name` you may need to split. A `PD-self` file that names no
    author credits the uploader of its first version, `"Name (uploader)"`:
    the uploader is who released it (sprint 029, where one gave an empty
    citation);
  - **organisations** (an institution, a centre, a college, a studio of
    two partners) are written as a `name`, and the Google Art Project's
    link text and Wikidata template text are dropped from the author and
    the title (sprint 028). Since sprint 050 a group, a trust or partners
    are organisations too ("Classical Numismatic Group" was split into
    family and given); a catalogue's "Family, Given" is read as a person,
    with a role after it dropped (the BnF's "Desbuissons, Edouard
    (1827-1908). Auteur du texte"); and a title loses a Wikidata label's
    text (`label QS:Les,…`), a DPLA identifier (`- DPLA - <hash>`) and a
    Library of Congress number (`LCCN…`);
  - **the date**, with `circa` for "c." or "circa", and a date BC as
    `"1504 BC"`, the form `published` takes since sprint 027 (sprint 026
    found "c. 1504 BC" written as AD 1504). A span ("1941-01-01/1945-12-31", or NARA's "between 1941 and 1945"
    since sprint 030) is written as circa its first year, with a warning to check it (sprint
    028 found one written as an exact day).
- **Four institutions' files are read further, and NARA's through DPLA** (sprint 033, korg 3478:
  most of sprint 030's authors still rewrote these by hand, writing credit
  lines and NARA series names as authors). It reads the file page's
  wikitext, and for a Wellcome file the Collection's own catalogue record.
  Every other file is written as before. Each is tested on a real Keeping
  Watch file kept in `fixtures/`.
  - **NARA** (a `NARA-image-full` page): the record's series is the
    `container` ("World War II Posters, National Archives and Records
    Administration"), the agency the author (the last unit of NARA's
    creator, said on stderr with the whole of it, so a parent can be named
    instead: the poster's "Bureau of Special Services" is the Office of War
    Information's), and its identifiers the `number` ("NAID 514214,
    44-PA-726A"). A creator who is a person (a presidential library's
    donor) is not written as the author.
  - **US Navy** (a `PD-USGov-Military-Navy` file, or a Navy image ID): the
    photographer from "photo by …" in the author or the description, with
    rank and rate taken off ("Mass Communication Specialist 2nd Class Erika
    N. Jones" is Jones, Erika N.); the container the Naval History and
    Heritage Command; the Navy image ID the `number`.
  - **Wellcome Collection** (a Wellcome Images file): the container, the
    creator from the Collection's catalogue record, and the image number
    (`L0000024`). Where that record is a book the image is a plate from,
    the book goes in the container ("The history of nursing in the British
    Empire, Wellcome Collection"), no author is written, and stderr names
    the book's author, who did not make the plate.
    A media citation's `number` is set after its container in the entry.
  - **DPLA** uploads (a `{{DPLA metadata}}` page, or `- DPLA - <hash>` in
    the title; sprint 050), whose Artist is an agency's path and a date
    ("Department of State. Agency for International Development.
    1961-10/1/1979"): the author is the last unit, said on stderr with the
    whole path, and a NARA record, as its credit line says, has NARA as
    its container and its identifier as the `number` ("NAID 19999523").
    A date in brackets after the path ("(1836 - 1849)") is not a unit
    (sprint 057; it was written as the author in sprint 051).
  - **Library of Congress** (a `{{LOC-image}}` page, or an `LCCN` in the
    title; sprint 057, korg 3557): the division is the `container`
    ("Library of Congress Prints and Photographs Division"), the LCCN the
    `number` ("LCCN 2004676518"), and a collection in the Artist field is
    not written as the author; stderr says so, with the record's "Photo
    by …" note when it has one, to check against the catalog.
- **`--page N`** takes one page of a PDF or DjVu on Commons as a JPEG (a
  scanned book's plate), named `<short-name>-pN.jpg`, and cites the file
  page with `?page=N`.
- **`--jpeg`** converts what it fetched to JPEG, and the **`jpeg`**
  command converts a page you cropped yourself; both composite a PNG's
  transparency onto white first (sprint 026's Frere engraving turned
  black).
- **`crop SRC DEST --box LEFT,TOP,RIGHT,BOTTOM`** cuts a box, in the
  image's pixels, out of a page image from outside Commons (a scan from the
  Internet Archive or a library), scales it down to `--width` (default 960) and writes a JPEG (sprint 029: authors cropped by hand). Cite such
  a page as the work it is from, with its own `media` citation.
  `--rotate 90|180|270` first turns a page printed sideways upright, that
  many degrees clockwise, so the box is in the upright page's pixels
  (sprint 033: a book plate printed sideways needed PIL by hand).
- The JPEG conversion needs Pillow, declared in the script's inline
  metadata (korg 3404). The script's shebang runs it under `uv run
--script`, and run with a `python3` that lacks Pillow, a command that
  converts runs itself again under `uv` (sprint 029: in sprint 028 `--jpeg`
  worked only under `uv run`). Everything else is standard library.
- Anything but public domain or CC0 gets a caption credit, which the page
  builds from the `media` citation (docs/design.md §Citations). Write no
  credit or caption line under the image yourself.
- `test_commons_media.py` is its test (`just check` runs it; no network).

Commons metadata is what uploaders typed. Open the file page and look at the
image before you use it: the licence is stated there, and a file's name does
not always say what it shows.
