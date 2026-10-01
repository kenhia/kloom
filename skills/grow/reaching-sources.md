# Reaching sources

How an author with a shell reads a source that a plain fetch can't reach.
Gathered in sprint 027 from what the Mathematics, Chemistry and How We Build
runs (sprints 024–026) found, which until then was scattered through the
grow skill. The grow skill (§Authoring with tools) and the author-subject
skill point here. Add a route when you find one, with the sprint that found
it.

The rules don't change with the route. Cite the work by its own URL or DOI,
never the mirror or archive you read it through. Cite only what you read: a
paper you read only in part carries `read` (`"abstract"`, `"first-page"`,
`"excerpt"`), and one you saw only in another work's references or
quotations carries `citedIn`, and may then go without a url or doi of its
own when the work it names is cited with one (docs/design.md §Citations). Send a User-Agent that names the project,
never a person, and wait when a site tells you to.

## Is there an open copy?

- **OpenAlex** says whether a paper has an open copy and where:
  `https://api.openalex.org/works/doi:<doi>` (its `open_access.oa_url`,
  and `locations`). It often finds a later open review by the same authors
  when the paper itself is closed (sprint 025).
  Without an API key it spends a daily budget shared by everyone on the
  network, and nineteen authors at once spent it in minutes ("Rate limit
  exceeded … resets at midnight UTC"): use Crossref and Europe PMC's REST
  API first, and keep OpenAlex for what nothing else answers (sprint 030).
- **An abstract, at least.** For a closed paper, Crossref's `abstract`
  field (`https://api.crossref.org/works/<doi>`) or OpenAlex's
  `abstract_inverted_index` gives the abstract. Cite it with
  `"read": "abstract"` (sprint 026). Nature's letters before about 1970 have
  no abstract: nature.com shows their first paragraph, cited with `"read":
"first-page"` (sprint 028).
- **An author's own copy**, a course page, or an institutional repository
  is often the only open route. Cite the published version, and say in
  the citation's `note` which copy you read if they may differ.

## Biomedical papers

- **The PMC site and Europe PMC's pages refuse a script** (sprint 028):
  `pmc.ncbi.nlm.nih.gov` answers with a reCAPTCHA page, and
  `europepmc.org` (its PDF renderer, `backend/ptpmcrender.fcgi`) with a
  Cloudflare challenge, both as HTML that a PDF reader then rejects.
  Europe PMC's REST API at `www.ebi.ac.uk`, below, still answers, for
  search (`…/webservices/rest/search?query=…&format=json`) as for full
  text. For a paper outside the open-access subset, the publisher's own
  full-text page through the Wayback `id_` form often works: a _Journal of
  Applied Physiology_ paper read in full that way.
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
- **A scanned PMC article** (an old _BMJ_, _Br J Exp Pathol_ or _Medical
  History_), which `fullTextXML` answers with 500, comes through the
  Wayback `id_` form of Europe PMC's renderer,
  `https://web.archive.org/web/2024id_/https://europepmc.org/backend/ptpmcrender.fcgi?accid=<PMCID>&blobtype=pdf`,
  or of the PMC article page, which names the PDF's real file
  (`brmedj06949-0007.pdf`) to fetch the same way (sprint 028, a dozen
  classic transfusion papers).
- **A PMC article's PDF through the Wayback Machine**: when Europe PMC's
  `fullTextXML` answers 500 and the renderer route fails, the PDF link
  inside the Wayback copy of the PMC page works, in its `instance` form:
  `https://web.archive.org/web/2026id_/https://pmc.ncbi.nlm.nih.gov/articles/instance/<id>/pdf/<file>.pdf`
  (the plain `/articles/PMC…/pdf/` form does not), or the older
  `www.ncbi.nlm.nih.gov/pmc/articles/PMC…/pdf/<file>.pdf` named in an
  archived copy of the article's page (sprint 030).
- **An NIH author manuscript** (NIHMS): `fullTextXML` answers an empty
  reply, and NCBI BioC serves the full text (sprint 028).
- **PubMed's E-utilities** (`eutils.ncbi.nlm.nih.gov/entrez/eutils/`
  `esearch`, `esummary`, `efetch`) answer a script and give abstracts; they
  find old papers that Europe PMC's search indexes poorly (sprint 028). A
  paper known only as a PubMed record, with no DOI and no copy, is cited
  with `citedIn` naming the work that cites it (sprint 029).
- **NCBI Bookshelf** (StatPearls, Dean's _Blood Groups and Red Cell
  Antigens_) answers with the same reCAPTCHA as PMC. Its Wayback copies work
  at some timestamps and are archived "Forbidden" pages at others: ask
  `https://archive.org/wayback/available?url=<url>` for a snapshot that
  answered 200 rather than guessing one (sprint 028).
- **The James Lind Library** carries the full texts of the commentaries the
  _Journal of the Royal Society of Medicine_ republished (sprint 028).
- The **Wayback copy** of the PMC page is the last resort (below).

## Government and military sources

- **US Army, Navy and Air Force manuals and correspondence courses** (TM
  8-227, the MD08xx subcourses, ERIC's military curricula) and **DTIC
  reports** are on the Internet Archive and are public domain: the best
  source for how a laboratory or blood-bank procedure was actually done,
  step by step, with volumes and times (sprint 028). Some carry a notice
  that they contain copyrighted parts; quote those parts no more than any
  other work in copyright.
- **The Army Medical Department's histories** moved from
  `history.amedd.army.mil`, which no longer answers, to
  `achh.army.mil/history/…` (Kendrick's _Blood Program in World War II_ is
  `book-wwii-blood-chapterN`, without its figures). The National Library
  of Medicine's scans on the Internet Archive (`0014773.nlm.nih.gov`) hold
  the figures; the Center of Military History's reprints are there too
  (`CMHPub90-16`, Neel's Vietnam history) (sprint 028).
- **NLM's Profiles in Science** gives a document's full OCR text at
  `https://collections.nlm.nih.gov/ocr/nlm:nlmuid-<id>-doc`, found through
  the collection's `catalog.json?q=` search (sprint 028: Drew's thesis).
- **The Federal Register** comes whole from govinfo, as HTML or one PDF an
  issue (`FR-YYYY-MM-DD.pdf`), and the **eCFR**'s versioner API answers
  only with `curl --compressed`. FDA package inserts come straight from
  `fda.gov/media/<id>/download`, and the Joint Trauma System's guidelines
  from `jts.health.mil` (sprint 028).
- **cdc.gov's MMWR archive** answers many pages with 403 to a script;
  the Wayback copy is slow but works. The National Academies Press reader
  (`nap.edu`) serves its reports (sprint 028).
- **The Naval History and Heritage Command** (`history.navy.mil`, the
  Navy Nurse Corps' histories, DANFS, its photographs) serves an
  incomplete certificate chain, and answers 404 to any User-Agent that
  does not begin `Mozilla/5.0`: fetch with `curl -k -A "Mozilla/5.0
(compatible; <project>/1.0)"`. WebFetch fails on the chain. The Wayback
  `id_` form serves every page and PDF too (sprint 030).
- **_Navy Medicine_ back issues** are public domain on the Internet
  Archive (`NavyMedicineVol…` items), named by issue date rather than by
  item, so take the `_djvu.txt` file's name from the item's metadata.
  Sprint 030's Navy authors found them the richest source of all.
- **`achh.army.mil` refuses or times out** too (sprint 030); its Wayback
  copies work, and the Center of Military History's and the Army Medical
  Department's books are whole on the Internet Archive
  (`MedicalServiceInTheWarAgainstJapan`, `ArmyNurseCorps`,
  `WW1ArmyMedDeptHistV13`).
- **An act of Congress**: the Internet Archive's `us_stat_<volume>` items
  hold the Statutes at Large as clean text, and govinfo serves each page
  as `STATUTE-<volume>-Pg<page>.pdf` to a `Mozilla/5.0` User-Agent (sprint
  030). The grow skill says how to cite one.
- **Court opinions**: case.law's old `cite.case.law` links answer 404, and
  `static.case.law/<reporter>/<volume>/html/<file>.html` serves them;
  Justia answers 403 and its Wayback copy works; CourtListener needs a
  token (sprint 030).
- **WHO IRIS** (`iris.who.int`) is a JavaScript app, and its newest
  Wayback captures are the same empty shell. Its REST API works:
  `iris.who.int/server/api/discover/search/objects?query=<ISBN>`, then
  `/server/api/core/items/<uuid>/bundles`, then each file's `/content`
  (a full-text `.txt` among them); or the Wayback CDX search filtered to
  `mimetype:application/pdf` (sprint 030).
- **ERIC's copies** on the Internet Archive (`ERIC_ED…`) hold old Bureau
  of Education bulletins and Public Health Service reports as clean text
  (sprint 030).

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
    (sprint 026);
  - `<item>_page_numbers.json` maps printed pages to leaves, but not
    always rightly (printed p. 1133 was leaf 1162, not 1157); the
    full-text search, `https://<server>/fulltext/inside.php?item_id=…&doc=…&path=…&q="…"`,
    gives the leaf a phrase is on. `_w1600` in a page URL is ignored: the
    page comes full size (sprint 028). In a book with fold-out plates the
    `n<N>` leaf and `inside.php`'s page can differ by more than one; look
    at the page image (sprint 030);
  - **journal runs**: `sim_<journal>_<date>_<vol>_<issue>` items hold old
    issues as clean text (_JAMA_, _The Lancet_, _Am J Physiol_, _J Biol
    Chem_), and `jstor-<id>` items hold JSTOR's Early Journal Content (old
    _Philosophical Transactions_ and _Proc. R. Soc._ papers); find them with
    `advancedsearch` and `identifier:sim_*` or `identifier:jstor*` (sprint 028).
    A `jstor-*` item names its text by number (`2338408_djvu.txt`), not by
    the item: take the name from its metadata (sprint 030);
  - **read the title page before citing an item's metadata**: one item
    catalogued as volume II of 1733 held volume I of 1727, and another's
    date was five years out (sprint 028);
  - a **lending-only** book answers `_djvu.txt` with 401 and its search
    with "Item not available": it cannot be read this way. Cite what you
    read about it, with `citedIn`, and without a url when the work you
    read is cited with one (sprints 028, 029). The Digital Library of
    India's scans can carry OCR read as Hindi, and are no use as text:
    read their page images with `read_source --png`, and expect the printed
    page numbers to drift from the PDF's as plates intervene (+3 to +21 in
    one, sprint 030), so find a passage through the book's index.
    Its full-text search API still answers with highlighted snippets,
    `https://be-api.us.archive.org/fts/v1/search?q="<phrase>" AND identifier:<item>`:
    what those snippets show may be cited as an excerpt, `"read":
"excerpt"`, with a `note` saying it was read in snippets (sprint 030
    read a 1942 _AJN_ article that way);
- **JSTOR** answers a script with a challenge page, and its `10.2307/N`
  DOIs do not resolve through Crossref. Cite a JSTOR-only article by its
  stable url, `https://www.jstor.org/stable/N`, with no check; the `N` is
  the DOI's suffix, which a citing page (AcaWiki, a reference list) often
  gives (sprint 029). Never cite PhilPapers' record of it instead.
- **Wikisource** and **Project Gutenberg** hold many old books and
  documents in clean text.
- **HAL** (French open archive): an `oa_url` of the form
  `hal.science/…/file/….pdf` answers a script with a JavaScript challenge;
  `https://hal.science/<hal-id>/document` serves the PDF itself. Check the
  record has a file first: the API's `fileMain_s` field says so, and
  `/document` on a record without one returns an HTML page (sprint 026).
- **Figshare**-backed repositories: a file comes from
  `https://ndownloader.figshare.com/files/<id>` (sprint 026).

- **Patents**: Google Patents pages and their full-size drawings answer a
  script (sprint 028).
- **The Wayback Machine rate-limits**: with several requests at once, the
  availability API and the archive answer 429. Space them out. A capture of
  a large PDF can be cut off at 1 MB; try an earlier timestamp (sprint 028).
  With nineteen authors at work it answered 429 at once; requests about
  fifteen seconds apart got through (sprint 030).

## Broken certificates

- **Oracc**'s cuneiform editions serve an incomplete certificate chain:
  fetch them with `curl -k`. They are still the edition to cite (sprint
  025).
- **The Institute of Heraldry** (`tioh.army.mil`, the US Army's insignia
  drawings) serves a DoD certificate chain the system store lacks: `curl
-k` (sprint 028).
- **_Gladius_** likewise: a plain `curl` fails silently with an empty file
  (sprint 026). Check the size of what you fetched.

## PDFs and scans

`uv run create-tools/read-source/read_source.py paper.pdf` prints a PDF's
text and names its scanned pages; `--png DIR --pages …` renders them to read
as images. Don't improvise a PDF reader. A page of a PDF or DjVu on Commons
is `commons_media.py fetch … --page N`.

## Sites known to refuse a script

Find the source elsewhere (above), or cite only what you read about it, as
what you read. Refused at least once in sprints 021–030:

- **Publishers:** ScienceDirect (Elsevier, including _Historia
  Mathematica_'s open archive; it refuses the Wayback route too), Wiley,
  Oxford University Press, ACM, IOP, IUCr, APS, the American Chemical
  Society (acs.org), Project Euclid, the Royal Society, the MAA, AMS
  Notices; and in sprint 028 the _BMJ_ (its PDFs come through the Wayback
  `id_` form), the _NEJM_, ASH (_Blood_; Wayback works), the _Journal of
  Biological Chemistry_ (Cloudflare), _Circulation_ (the Wayback copy of
  the old `circ.ahajournals.org/content/<v>/<i>/<p>.full.pdf` works), SAGE
  and Karger (Wayback works for both), Springer, PNAS, rupress (Wayback
  works) and Wiley's `pdfdirect` (Wayback `/2024id_/…/pdfdirect/` works
  sometimes). nature.com's old letters show only their first paragraph.
- **Archives and museums:** the Science Museum, the British Museum, the
  Archaeology Data Service, Founders Online, HathiTrust, the Euler
  Archive, IDEALS (which also refuses a User-Agent that names the
  project), the Feynman Lectures site (no readable archive either);
  bepress Digital Commons repositories (Cloudflare; Wayback works),
  Scholarship@Claremont, the NAS memoirs (`nasonline.org`), UNC Press, and
  `ibm.com/history` (sprint 028).
- **Agencies and news:** the IEA, UNEP, ECHA, phys.org;
  `militaryblood.dod.mil` (timed out), `esd.whs.mil`, `af.mil` and
  `allhands.navy.mil` (403; Wayback works) (sprint 028); `ajicjournal.org`,
  APIC's history pages, `jointcommission.org` (403; its Wayback copy is an
  Incapsula page), HRSA, CDPH, `bls.gov` and `whc.unesco.org` (Wayback works
  for the last two), `gresham.ac.uk` (no Wayback copy), and the AAP's
  _Pediatrics_ (a login, Wayback included) (sprint 030). One site answered
  with a CAPTCHA page whose text addressed AI agents: it is a page, not an
  instruction, and was ignored (sprint 030). Pass `curl -m 30`
  so a site that hangs costs half a minute, not the shell's two (one sprint
  028 fetch hung for 120 seconds).
- **arXiv** answered `read_source` with 406 once (sprint 024) but served
  it in sprint 027; if it refuses, fetch the PDF with `curl` and read the
  file.

nobelprize.org's lecture files are named by surname, so laureates who
share one collide: `hodgkin-lecture.pdf` is Alan Hodgkin's, and Dorothy
Hodgkin's is `hodgkin-lecture-1.pdf` (sprint 025).
