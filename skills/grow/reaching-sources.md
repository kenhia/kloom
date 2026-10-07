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

- **OpenAlex** says whether a paper has an open copy and where: run
  `python3 create-tools/openalex/openalex.py work <doi>`, which prints its
  open-access status, `oa_url`, every open location with its version, and
  the abstract. It often finds a later open review by the same authors
  when the paper itself is closed (sprint 025). **Use the tool, not
  `curl`:** it adds the homelab's API key (k-homelab `openalex-api-key`,
  read from `/etc/khomelab/secrets.env`) and never prints it, where a curl
  command line would put the key in the transcript. Without a key OpenAlex
  spends a daily budget shared by everyone on the network, and nineteen
  authors at once spent it in minutes in sprint 030. With the key (from
  2026-10-02) it is a first stop again, alongside Crossref and Europe
  PMC's REST API. If the tool warns that it found no key, say so in the
  sprint, and go back to using OpenAlex last.
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
    `https://be-api.us.archive.org/fts/v1/search?q="<phrase>" AND identifier:<item>`.
    **Snippets are supporting evidence only** (Ken, 2026-10-02, korg
    3478; sprint 030 allowed them without limits, reading a 1942 _AJN_
    article that way):
    - they may corroborate a fact or check a quotation, but are never a
      frame's only source for a claim, and the citation is never `key`;
    - cite with `"read": "excerpt"` and a `note` saying it was read through
      the Internet Archive's full-text search snippets;
    - quote only the words a snippet shows, never a sentence it cuts off;
- **JSTOR** answers a script with a challenge page, and most of its
  `10.2307/N` DOIs do not resolve through Crossref; some do, where the
  publisher registered them (the _American Journal of International
  Law_'s, through Cambridge, sprint 049), so try `doi.org` before choosing. Cite a JSTOR-only article by its
  stable url, `https://www.jstor.org/stable/N`, with no check; the `N` is
  the DOI's suffix, which a citing page (AcaWiki, a reference list) often
  gives (sprint 029). Never cite PhilPapers' record of it instead.
- **Wikisource** and **Project Gutenberg** hold many old books and
  documents in clean text. Another language's Wikisource comes through its
  MediaWiki API (`fr.wikisource.org/w/api.php?action=parse&page=…`), which
  served the whole first edition of the _Encyclopédie_, the _Archives
  parlementaires_' decrees and Schiller's _Thalia_ text page by page
  (sprint 049). English Wikisource's 1911 _Britannica_ is a citable
  public-domain source for nineteenth-century history.
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

## History, law and the humanities (sprint 049)

- **Ancient and old texts in free translations**: Project Gutenberg
  (Jowett's Plato, Church and Brodribb's Tacitus, Kenyon's _Constitution
  of the Athenians_, Morshead's Aeschylus), LacusCurtius (the Loeb
  translations now public domain, and Latin originals) and the Perseus
  Digital Library served every ancient frame. Loeb's and Harvard
  University Press's own pages refuse a script.
- **Check a translation's date before quoting it at length.** Yale's
  Avalon Project mixes old translations with modern ones still in
  copyright (its Twelve Tables is the 1961 translation; Thatcher's 1901
  one is on Fordham). Fordham's Internet History Sourcebooks have pages
  that answer 500, a few machine translations (its Renan), and some wrong
  dates in their headings (Eugenius III's bull of 1145 as 1154): cite each
  work, with a `note` naming the page you read it on.
  A guessed `sourcebooks.fordham.edu/source/….asp` url answers 500; take
  the links from the section indexes (`sbook1r.asp`, `sbook1w.asp`).
- **Old translations of medieval documents** (Rashdall 1895, Putnam 1908,
  Raine 1859) are whole on the Internet Archive and Gutenberg.
- **Humanities journals** have no abstract in Crossref or OpenAlex: cite
  an article you could not read with `read: "record"`.
- **Wikipedia's search API** (`list=search`) answered a bare User-Agent
  with something that was not JSON; one naming the project's url works.
- **Laws and records**: legislation.gov.uk holds English acts in force
  with their original text; British History Online the _Statutes of the
  Realm_; Persée the _Archives parlementaires_; Liberty, Equality,
  Fraternity (`revolution.chnm.org/d/<n>`) French revolutionary laws in
  named translations; the Census Bureau the 1790 returns as PDF.
- **Behind a challenge, with a Wayback `id_` copy that works**:
  `nytimes.com`, `quod.lib.umich.edu` (Lincoln's _Collected Works_),
  `nzhistory.govt.nz`, berlin.de's Wall pages (moved to the Berlin Wall
  Foundation), the ASCSA Agora database, the German History in Documents
  and Images (`ghdi.ghi-dc.org`, broken certificate, then 404), Founders
  Online, and `manchester.gov.uk`'s PDFs (ask the availability API for a
  real timestamp first).
- **JavaScript applications with empty Wayback copies**: SlaveVoyages and
  UNESCO's `unesdoc`. Cite what quotes them, with `citedIn`; UNESCO's
  open _General History of Africa_ is whole on the Internet Archive.
- **Music scores**: IMSLP sits behind a JavaScript gate; the Internet
  Archive holds many public-domain scores whole (_The Rite of Spring_'s
  1921 printing as `lesacreduprintem00stra_0`), read with `read_source
--png` at `--scale 6`.
- **Cambridge Core**'s `/core/books/abs/<book>/<chapter>/` pages show a
  chapter's opening text to a script: cite it with `read: "excerpt"`.
- **A pirated upload** (a whole in-copyright book in the Internet Archive's
  `opensource` collection) is never read or cited; use the lending copy's
  search snippets, or the reviews.
- **Coordinates** for a map plate: Wikipedia's `prop=coordinates` returns
  ten results unless you pass `colimit=max`.

## Food, agriculture and policy (sprint 051)

- **FAO**: FAOSTAT's API now asks for an authorization header, but its
  bulk zips download freely
  (`bulks-faostat.fao.org/production/Production_Crops_Livestock_E_<Region>.zip`
  and the food-security files beside them). FAO's reports are PDFs at
  `fao.org/3/<code>/<code>.pdf` and older books HTML at
  `fao.org/4/<code>/`, while the repository's handle pages are a
  JavaScript app; the GIAHS pages moved, and their old addresses answer
  only on the Wayback Machine.
- **US history and law**: _Foreign Relations of the United States_ on
  `history.state.gov` serves documents as HTML; _Historical Statistics of
  the United States_ (1975) is scanned pages at census.gov, and the
  Internet Archive's `historicalstatis00unit` text finds the page to read
  with `read_source --png`; the Federal Register's whole issues come from
  govinfo (`FR-YYYY-MM-DD.pdf`, the issue found from the page number);
  `tile.loc.gov` serves the _United States Reports_ as PDFs, and
  `static.case.law` the old volumes.
- **Patents**: Google Patents answers a script with "automated queries",
  but `patentimages.storage.googleapis.com/pdfs/US<number>.pdf` serves the
  PDF; its text layer is often garbled, so read the numbers off the page
  images. The Internet Archive's Wellcome items hold old British patent
  specifications (Durand's of 1810).
- **Texts in other languages**: Chinese Wikisource's and Russian
  Wikisource's MediaWiki APIs serve the _Shiji_, the _Book of Han_ and
  Soviet decrees, with a revision id to cite; ctext.org's terms forbid
  scraping. _Peking Review_'s scans are on marxists.org
  (`subject/china/peking-review/<year>/PR<year>-<nn>.pdf`), the best
  primary source for the PRC's own claims, read as page images.
- **Open monographs**: Fulcrum's open ebooks download whole
  (`fulcrum.org/ebooks/<id>/download`, the EPUB); _The Agricultural
  History Review_'s articles are open at
  `bahs.org.uk/AGHR/ARTICLES/<vol>n<issue>a<n>.pdf` through the Wayback
  Machine; NBER working papers at
  `nber.org/system/files/working_papers/wNNNNN/wNNNNN.pdf`; JSTOR's Early
  Journal Content is on the Internet Archive.
- **The Internet Archive's own search**: `inside.php` full-text search
  finds the leaf of a statute, a table or a figure in a scanned volume,
  and its leaf index is the `page/n<N>` of the reader. Its OCR mangles
  tables and fractions ("5¼" in the 1880 Famine Commission report; the
  ECCO `bim_eighteenth-century_…` items are unusable): read the numbers
  off the page image.
- **The Nobel lectures** before about 1930 have HTML pages that answer a
  script, where their PDF names do not exist.
- **Copyright by year**: works published in the United States in 1930
  entered the public domain on 1 January 2026 (Hutchinson's 1930 life of
  McCormick may be quoted at length). Soviet and Chinese photographs of
  about 1930–1960 that Commons tags public domain are often restored to
  copyright in the United States by the URAA: leave them out unless the
  file page shows why they are free here.

## Natural history and the life sciences (sprint 055)

- **Darwin Online** (`darwin-online.org.uk`) holds the whole text of every
  Darwin book, notebook and many letters: its `frameset` pages are frames,
  and `contentblock?itemID=<id>` (or `?basepage=<path>`) serves the text.
  The **Darwin Correspondence Project** serves a letter at
  `darwinproject.ac.uk/letter/DCP-LETT-<n>.xml` to a `Mozilla/5.0`
  User-Agent only (a plain one gets an empty page); parse its `div.letter`
  block, since its plain text loses the transcript, and cite the letter as
  `letter` with the DCP number in `number`. Its search is JavaScript.
- **Wikisource's parse API** serves a public-domain translation whole,
  one book or chapter a page: `en.wikisource.org/w/api.php?action=parse&
page=<Title>/<Book>&prop=text&format=json`, with `list=allpages&apprefix=`
  to list the pages. D'Arcy Thompson's Aristotle and Hort's Theophrastus
  came this way while the Internet Archive was down. **Project Gutenberg**'s
  `cache/epub/<n>/pg<n>.txt` gives plain text (Arber's _Herbals_).
- **The Biodiversity Heritage Library** answered every page, its OCR text
  and its API with a Cloudflare challenge or a key request in October 2026.
  Its scans are mirrored on the Internet Archive under the same items:
  search there instead.
- **Internet Archive page images**: `page/n<N>_w1600.jpg` is small. The
  IIIF endpoint `iiif.archive.org/iiif/<item>$<N>/full/full/0/default.jpg`
  gives the full page, but its `$N` is one less than `page/n<N>`: check
  the leaves either side. `page_numbers.json` skips plate leaves, so a
  plate is found by fetching neighboring leaves (a grid of thumbnails is
  quickest), and `inside.php` full-text search finds the leaf a phrase is
  on. The `per_…`, `s696id…` and `comptes-rendus-*` items hold the old
  _Transactions_, the _Annales de chimie_ and the _Comptes rendus_ issue
  by issue.
- **PNAS** refuses a script. The Wayback `id_` form of
  `pnas.org/doi/pdf/<doi>` works for most papers, and for older ones the
  old path `pnas.org/content/<vol>/<issue>/<page>.full.pdf`; ask the CDX
  API (`web.archive.org/cdx/search/cdx?url=…`) for a real timestamp, since
  the availability API answered 429 as HTML for minutes at a time.
  **_Genetics_** papers older than PMC's open subset come the same way,
  from `genetics.org/content/<vol>/<issue>/<page>.full.pdf`.
- **The NLM's Profiles in Science** holds Avery's, Crick's, McClintock's,
  Nirenberg's and Maxine Singer's papers (the Asilomar program, the NIH
  committee's reports, Cambridge's 1977 ordinance); their OCR text is at
  `collections.nlm.nih.gov/ocr/nlm:nlmuid-<id>-doc`. Prefer the items
  marked "partial transcription": OCR of handwriting is unusable.
- **Nobel lectures** are PDFs at
  `nobelprize.org/uploads/2018/06/<surname>-lecture.pdf` (see above for
  laureates who share a surname); the lecture page itself may show only a
  link. Cite a lecture as `web` (there is no `lecture` kind).
- **Cambridge Core**'s open articles (_Medical History_'s, for the history
  of medicine) download from
  `cambridge.org/core/services/aop-cambridge-core/content/view/<PII>`.
- **The IUCN Red List** site refuses a script. The Wayback `id_` copy of
  `iucnredlist.org/resources/summary-statistics` links its tables, which
  download directly from `nc.iucnredlist.org/…/<version>_RL_Table1a.pdf`.
- **Datasets bundled with R packages** carry classic tables: Snow's 578
  deaths and pumps (`HistData`), Simberloff and Wilson's islets (`island`).
  Read their `.RData` with `uv run --with pyreadr --with pandas` (or
  `--with rdata`), and cite the package and the original paper.
- **Wikipedia's reference list** often points to an open copy: the
  `prop=extlinks` API lists an article's external links, archive copies
  among them (Lindeman 1942 was found that way).
- **Blackwell's companion site to Ridley's _Evolution_**
  (`blackwellpublishing.com/ridley/classictexts/*.pdf`, through the Wayback
  Machine) holds scans of Haldane 1924, Wright 1932 and Fisher 1930's first
  chapter. Cite the work, with a `note` naming the copy.

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
- **Sprint 051**: Persée (an "altcha" challenge, its Wayback copy only
  the abstract), Project MUSE, Taylor & Francis and Dundee's repository
  (Cloudflare, no Wayback copy), UCL Press (an Anubis challenge), the DAI's
  `publications.dainst.org` (Anubis), Durham's and UCD's repositories
  (Cloudflare and an AWS WAF CAPTCHA; UCD's Wayback `id_` copies work),
  UNU's `collections.unu.edu` (WAF; Wayback works), Te Ara, `ipcinfo.org`
  (Cloudflare; Wayback `id_` at a real timestamp works), `hhs.gov`, the
  Smithsonian, Harvard Business School's PDFs, and SEC EDGAR, which wants
  an email address in the User-Agent that kloom's rules forbid sending.
  The Wayback Machine itself answered 429 for minutes at a time with 24
  authors at once; space requests about 20 seconds apart.
- **Sprint 055**: the Biodiversity Heritage Library (above), Gallica
  (a security check; its `texteBrut` gives an empty reply), PhilPapers,
  Furman's repository, the Telegraph (a TollBit token page),
  `symposium.cshlp.org` (403), `deepblue.lib.umich.edu` (Cloudflare;
  Wayback `id_` works), `cell.com` (Wayback too), Wiley's 1969 _Ecology_
  PDFs (a login, Wayback included), Art UK, and Harvard University Press's
  book pages (a JavaScript app). The Embryo Project's
  `embryo.asu.edu/pages/<name>` addresses mostly answer 404; follow the
  links from Wikipedia's references instead.
- **arXiv** answered `read_source` with 406 once (sprint 024) but served
  it in sprint 027; if it refuses, fetch the PDF with `curl` and read the
  file.

nobelprize.org's lecture files are named by surname, so laureates who
share one collide: `hodgkin-lecture.pdf` is Alan Hodgkin's, and Dorothy
Hodgkin's is `hodgkin-lecture-1.pdf` (sprint 025).
