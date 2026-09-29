On 11 October 1964 **Doug McIlroy** of Bell Labs finished a memo with a
summary of what mattered most to him. The first point asked for ways of
"connecting programs like garden hose", screwing in another segment
whenever data had to be massaged another way. At the time Bell Labs did its
computing in batch, on IBM 7090 and 7094 machines fed with tape. Years later
**Dennis Ritchie** kept that page, yellowed, stuck by a magnet to his
office wall. It took eight or nine years, and Unix, for the hose to be
built.

## An idea on a blackboard

Unix had redirection from the start: a program read its _standard input_
and wrote its _standard output_, and the shell could point either at a
file. McIlroy wanted more. He proposed that commands be treated as
operators, with their input on the left and output on the right, so that
sorting a file, paginating it and printing it would be
`input sort paginate offprint`. He explained it one afternoon on a
blackboard. The others were intrigued and did nothing: the notation seemed
too radical, nobody could see how to tell a command's arguments from its
files, and one input and one output seemed too confining. "What a failure
of imagination!" Ritchie wrote afterwards.

## One feverish night

McIlroy persisted; Ritchie says he very nearly used his authority as their
manager to get pipes in. In McIlroy's telling, **Ken Thompson** finally
agreed and, "in one feverish night", wrote the `pipe`
system call, added pipes to the shell, and changed several programs,
among them `pr` and `ov`, to work as _filters_. "The next day saw an
unforgettable orgy of one-liners," McIlroy wrote. One shown off that first
day printed four columns with `roff file >ov>ov>`.

That was the first notation: `>` followed by a command meant "into that
command". It lasted only a couple of months. It needed quoting for any
argument, and it could be written backwards with `<` as well. Before a
public talk, to spare himself explaining it, Thompson proposed the vertical
bar. Describing pipes had taken almost a page of the Third Edition manual;
in the Fourth, it took four sentences.

The date is given two ways. Ritchie's history of 1979 says pipes appeared
in 1972. The Third Edition manual that first describes them is dated
February 1973, and McIlroy lists them under it; the Fourth, with `|`, came
that November.

![Doug McIlroy in 2011, grey-haired, in glasses and a tweed jacket, smiling a little](mcilroy.jpg)

## How a pipe works

A pipe is a buffer in the kernel with two ends, each a file descriptor;
the very first pipes used one descriptor for both, and the Fourth Edition
split them.
The plate draws `sort input | pr | opr`, Ritchie's own example. The shell
starts all three programs at once, with `sort`'s output (descriptor 1)
joined to `pr`'s input (descriptor 0), and `pr`'s to `opr`'s. The kernel
keeps what one has written and the next has not yet read; a writer that
fills the buffer waits, and so does a reader that empties it. None of the
programs knows. It reads and writes as if to files.

The genius of it, Ritchie thought, was that it used the very same commands
people typed alone every day. Multics could splice processing modules into
an input or output stream, but only modules written for the purpose.
Dartmouth's time-sharing system had _communication files_ that did very
nearly what pipes did, though Bell Labs did not know of them.

## A worked pipeline

Here is the pipeline style, run on the ninety-three words of McIlroy's
summary as Ritchie retyped it, to count its commonest words:

`tr -cs 'A-Za-z' '\n' < memo | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn | head -3`

| Stage                  | What it passes on                                    |
| ---------------------- | ---------------------------------------------------- |
| `tr -cs 'A-Za-z' '\n'` | each run of letters on its own line: one word a line |
| `tr 'A-Z' 'a-z'`       | the same words in lower case                         |
| `sort`                 | the words in order, so repeats sit together          |
| `uniq -c`              | each distinct word once, with its count              |
| `sort -rn`             | those lines, largest count first                     |
| `head -3`              | the first three: `4 to`, `4 should`, `3 it`          |

Six programs, none written for this job, and none of them changed.

## Filters, then a philosophy

Programs changed to fit. Nobody had imagined wanting `sort` to sort its
standard input, and Thompson made it a filter. He wrote `grep` for the
Fourth Edition, McIlroy `tr`, and Lee McMahon later `sed`. Error messages
were a problem: they went to the standard output, so they ran down the
pipe into the next program. After the Sixth Edition Ritchie added a third
stream, _standard error_, which the plate sends to the terminal.

McIlroy, with E. N. Pinson and B. A. Tague, wrote down the style that had
grown up, in the foreword to the
_Bell System Technical Journal_'s Unix issue of July 1978. Its second rule
begins: "Expect the output of every program to become the input to
another, as yet unknown, program." Pipes, McIlroy wrote, changed how they
thought about program design more than redirection ever had.

By the 1980s some thought the tools were growing too many options. Brian
Kernighan and Rob Pike said so in 1984, naming two new Unixes as examples:
AT&T's System V, and Berkeley's 4.2BSD, whose story is next.
