# commons-media

Images from Wikimedia Commons for a reading, with the `media` citation the
validator requires (sprint 006, written for the ai subject).

```sh
python3 create-tools/commons-media/commons_media.py search "Mark I Perceptron"
python3 create-tools/commons-media/commons_media.py fetch "File:Name.jpg" subjects/<subject>/frames/<frame> --as short-name [--width 960]
```

- `search` lists image files (not PDFs or video) matching the text, each
  marked `ok` when its licence is public domain, CC0 or CC BY(-SA), with its
  size and author.
- `fetch` refuses any other licence. It downloads a scaled copy into the
  frame directory as `<short-name>.<ext>`. Commons serves thumbnails only at
  fixed widths (120, 250, 330, 500, 960, 1280, 1920) and rounds a request
  up, so `--width` (default 960) takes the widest step no wider than
  asked. It warns when the file is over 350 KB; try `--width 500`. It
  prints
  the citation: file page url, author, date, licence and file name, from the
  file page's own metadata. Rewrite its `title` into a description of the
  work, and its `container` into where the work is from, as the curated
  frames do.
- Anything but public domain or CC0 gets a caption credit, which the page
  builds from the `media` citation (docs/design.md §Citations). Write no
  credit or caption line under the image yourself.
- An unknown author is left out of the citation, not written as "Unknown"
  (nor "AnonymousUnknown author" or 不明, which sprint 026 met). A date BC is
  left out too: `published` takes only an AD year, and the tool once wrote
  "c. 1504 BC" as 1504.
- Standard library only.

Commons metadata is what uploaders typed. Open the file page and look at the
image before you use it: the licence is stated there, and a file's name does
not always say what it shows.
