# commons-media

Images from Wikimedia Commons for a reading, with the `media` citation the
validator requires (sprint 006, written for the ai subject).

```sh
python3 create-tools/commons-media/commons_media.py search "Mark I Perceptron"
python3 create-tools/commons-media/commons_media.py fetch "File:Name.jpg" subjects/<subject>/frames/<frame> --as short-name [--width 800]
```

- `search` lists image files (not PDFs or video) matching the text, each
  marked `ok` when its licence is public domain, CC0 or CC BY(-SA), with its
  size and author.
- `fetch` refuses any other licence. It downloads a copy scaled to `--width`
  (default 800) into the frame directory as `<short-name>.<ext>`, and prints
  the citation: file page url, author, date, licence and file name, from the
  file page's own metadata. Rewrite its `title` into a description of the
  work, and its `container` into where the work is from, as the curated
  frames do.
- Anything but public domain or CC0 gets a caption credit in the reading
  (docs/design.md §Citations).
- Standard library only.

Commons metadata is what uploaders typed. Open the file page and look at the
image before you use it: the licence is stated there, and a file's name does
not always say what it shows.
