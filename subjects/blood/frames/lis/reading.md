By the 1960s a hospital laboratory could measure faster than it could write. Machines like the AutoAnalyzer turned out results by the hundred, and every one still had to be matched to a patient by hand. In the blood bank the stakes were higher: the right unit could be typed and crossmatched perfectly and still go to the wrong patient. Over the next thirty years the paper was replaced by a **[laboratory information system](kloom:e/laboratory-information-management-system)**, a computer that keeps the requests, the specimens, the results and, in the blood bank, every unit from donor to recipient.

## The paper day

Leonard Skeggs set out his own laboratory's daily routine, with AutoAnalyzers already running, as ten steps. Only one was done by a machine:

| Step | What was done                                                          |
| ---- | ---------------------------------------------------------------------- |
| 1    | Clotted bloods and requisition slips arrive in the laboratory          |
| 2    | Prepare sera                                                           |
| 3    | From the slips, make an identifying list of sera for each method       |
| 4    | Divide each serum into a sample cup for each test ordered              |
| 5    | Place the cups in each method's sampler tray, in the order of its list |
| 6    | Perform the analyses automatically                                     |
| 7    | Calculate all records                                                  |
| 8    | Record results on the identifying lists                                |
| 9    | Copy results from the lists onto the requisitions                      |
| 10   | Send the requisitions to the physician                                 |

Every arrow between those steps was a chance to copy a name or a number wrongly. In the blood bank the errors had names: the wrong specimen tested, a result transcribed wrongly, the wrong unit issued, the right unit hung on the wrong patient. When C. L. Honig and J. R. Bove reviewed the 70 deaths associated with transfusion reported to the Bureau of Biologics from 1976 to 1978, 38 were acute hemolytic reactions from ABO-incompatible blood, and "clerical confusion" caused 33 of the 37 in which the error could be found. A later review of the 256 transfusion deaths reported to the **[Food and Drug Administration](kloom:e/food-and-drug-administration)** from 1976 to 1985 found that half were from ABO-incompatible products, but put them down "primarily to managerial, not clerical, errors": a matter of who was allowed to hang blood and how they were trained, not only of handwriting. In New York State, among 1,784,600 red-cell transfusions in 22 months reported in 1992, blood went to the wrong person or of the wrong group once in 19,000, and three patients died. Most of those errors happened outside the blood bank: 43% solely from failing to identify the patient or the unit before transfusing, 11% from the person drawing the sample.

## Computers in the laboratory

The first systems were built by hospitals for themselves. At **[Massachusetts General Hospital](kloom:e/massachusetts-general-hospital)**, in an NIH-funded hospital computer project, Neil Pappalardo, Robert Greenes and Curt Marble wrote a language and database in 1966 and 1967 called **[MUMPS](kloom:e/mumps)**, the Massachusetts General Hospital Utility Multi-Programming System. It ran first on a DEC **[PDP-7](kloom:e/pdp-7)** and then a PDP-9, minicomputers, and was used for admissions and for reporting laboratory tests. Released into the public domain, it was carried to the PDP-8 and PDP-11 and spread through medicine; hospital laboratory systems were what it had been written for.

A system of this kind turns the paper day into a chain of checks. The request is entered once; the specimen gets a printed label with an accession number; the analysers' results arrive by wire; and the report goes back without being copied. In the blood bank it can refuse a release: a 1994 procedure from the University of Michigan had the computer read a bar-coded specimen number and unit number, compare the unit's bar-coded group with the one just typed and with the patient's history, quarantine any unit that disagreed, and give group O red cells until two concordant types were on record. With those checks it replaced the immediate-spin **[crossmatch](kloom:e/cross-matching)** for ABO, saving, by the authors' estimate, more than 100,000 workload units a year.

## A number for every unit

Bar codes reached blood bags in the late 1970s, in a scheme the American Blood Commission based on **[Codabar](kloom:e/codabar)**. It had flaws. The same donation number could turn up in two countries, or twice in one centre; product codes were five characters with a fixed meaning for each place, and ran out; there was no check character to catch a misread. In 1989 the International Society of Blood Transfusion asked its working party to replace it, and the first specification of **[ISBT 128](kloom:e/isbt-128)** was published and approved in 1994.

The plate draws its donation identification number, using the specification's own example: thirteen characters, a five-character facility code assigned by ICCBBA, a two-digit year and a six-digit serial, so that no number repeats for a hundred years. The Code 128 symbol carries a check character the scanner tests, and the printed number ends with a boxed character, K, for anyone who has to type it.

## What it cost

In March 1994 the FDA told the makers of blood bank software that their programs were medical devices: they had to register, follow the agency's manufacturing rules and file a premarket submission by March 1995. Every change since has had to be validated by the blood bank as well. And a system that can stop a wrong unit can also stop: the Michigan procedure kept the serological crossmatch for computer downtime, so the old manual way had to be kept ready for the hours when the new one failed. The next frame turns from records to reagents, to a card that makes the reading of a reaction a record in its own right.
