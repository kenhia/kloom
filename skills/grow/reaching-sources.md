# Reaching sources

How an author with a shell reads a source that a plain fetch can't reach.
Gathered in sprint 027 from what the Mathematics, Chemistry and How We Build
runs (sprints 024–026) found, which until then was scattered through the
grow skill. The grow skill (§Authoring with tools) and the author-subject
skill point here. Add a route when you find one, with the sprint that found
it.

The rules don't change with the route. Cite the work by its own URL or DOI,
never the mirror or archive you read it through. Cite only what you read: a
paper you saw only as an abstract carries `"abstractOnly": true`, and one
you saw only in another work's references or quotations carries `citedIn`
(docs/design.md §Citations). Send a User-Agent that names the project,
never a person, and wait when a site tells you to.

## Is there an open copy?

- **OpenAlex** says whether a paper has an open copy and where:
  `https://api.openalex.org/works/doi:<doi>` (its `open_access.oa_url`,
  and `locations`). It often finds a later open review by the same authors
  when the paper itself is closed (sprint 025).
- **An abstract, at least.** For a closed paper, Crossref's `abstract`
  field (`https://api.crossref.org/works/<doi>`) or OpenAlex's
  `abstract_inverted_index` gives the abstract. Cite it with
  `abstractOnly` (sprint 026).
- **An author's own copy**, a course page, or an institutional repository
  is often the only open route. Cite the published version, and say in
  the citation's `note` which copy you read if they may differ.

## Biomedical papers

- **Europe PMC** serves a PubMed Central article's full text when the PMC
  site refuses a script:
  `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`.
  It answers 500 for a scanned article, and often for others (sprint 025).
  It serves only PMC's open-access subset: an article free to read but not
  openly licensed (PNAS's, for instance; Europe PMC's search shows
  `isOpenAccess` `N`) comes back empty (sprint 026).
- **NCBI BioC** is the fallback:
  `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/<PMCID>/unicode`.
  It rate-limits (429) quickly.
- The **Wayback copy** of the PMC page is the last resort (below).

## Archives and repositories

- **The Wayback Machine's `id_` form** serves the page as it was, without
  the archive's frame: `https://web.archive.org/web/2024id_/<url>`. It
  serves many pages gzipped, so read every copy with `curl --compressed`,
  and `-L` to follow a `/web/<timestamp>/` link (sprints 021, 025). It
  works for many sites that refuse a script (RAND, AMS, Bell Labs'
  history pages, APS, PNAS, MDPI, CERN's press pages, nobelprize.org).
  It does not work for ScienceDirect.
- **The Internet Archive** for old books and journals:
  - an item's full text is `https://archive.org/download/<item>/<item>_djvu.txt`,
    often all you need for an old edition (sprint 024 read Peet's 1923
    Rhind papyrus that way);
  - when OCR is useless (old tables, the long s read as f), each page is an
    image, `https://archive.org/download/<item>/page/n<N>_w1600.jpg`, with
    `<N>` from the item's full-text search (sprint 025 caught a misprinted
    1744 Boyle table that way). Check every quotation against the page
    image where OCR may have dropped or changed words: one sprint 026 draft
    misquoted Moxon from the text layer;
  - when `/download/` answers 500, read the file from the storage path that
    `https://archive.org/metadata/<item>` gives (`server` and `dir`)
    (sprint 026).
- **Wikisource** and **Project Gutenberg** hold many old books and
  documents in clean text.
- **HAL** (French open archive): an `oa_url` of the form
  `hal.science/…/file/….pdf` answers a script with a JavaScript challenge;
  `https://hal.science/<hal-id>/document` serves the PDF itself. Check the
  record has a file first: the API's `fileMain_s` field says so, and
  `/document` on a record without one returns an HTML page (sprint 026).
- **Figshare**-backed repositories: a file comes from
  `https://ndownloader.figshare.com/files/<id>` (sprint 026).

## Broken certificates

- **Oracc**'s cuneiform editions serve an incomplete certificate chain:
  fetch them with `curl -k`. They are still the edition to cite (sprint
  025).
- **_Gladius_** likewise: a plain `curl` fails silently with an empty file
  (sprint 026). Check the size of what you fetched.

## PDFs and scans

`uv run create-tools/read-source/read_source.py paper.pdf` prints a PDF's
text and names its scanned pages; `--png DIR --pages …` renders them to read
as images. Don't improvise a PDF reader. A page of a PDF or DjVu on Commons
is `commons_media.py fetch … --page N`.

## Sites known to refuse a script

Find the source elsewhere (above), or cite only what you read about it, as
what you read. Refused at least once in sprints 021–026:

- **Publishers:** ScienceDirect (Elsevier, including _Historia
  Mathematica_'s open archive; it refuses the Wayback route too), Wiley,
  Oxford University Press, ACM, IOP, IUCr, APS, the American Chemical
  Society (acs.org), Project Euclid, the Royal Society, the MAA, AMS
  Notices.
- **Archives and museums:** the Science Museum, the British Museum, the
  Archaeology Data Service, Founders Online, HathiTrust, the Euler
  Archive, IDEALS (which also refuses a User-Agent that names the
  project), the Feynman Lectures site (no readable archive either).
- **Agencies and news:** the IEA, UNEP, ECHA, phys.org.
- **arXiv** answered `read_source` with 406 once (sprint 024) but served
  it in sprint 027; if it refuses, fetch the PDF with `curl` and read the
  file.

nobelprize.org's lecture files are named by surname, so laureates who
share one collide: `hodgkin-lecture.pdf` is Alan Hodgkin's, and Dorothy
Hodgkin's is `hodgkin-lecture-1.pdf` (sprint 025).
