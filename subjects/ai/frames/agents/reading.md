A chat model answers and waits. An _agent_ is given a goal and left to
pursue it: it plans, calls tools, reads what comes back and tries again,
sometimes for hours. Between 2022 and 2026 language models went from the
first to the second, and software engineering became the proving ground.

## Reasoning and acting

In October 2022 **Shunyu Yao** and six colleagues
published **ReAct**, which interleaved a model's written reasoning with
actions: search a knowledge base, read the result, reason again. The
reasoning traces, they wrote, help the model "induce, track, and update
action plans", while actions let it gather information it did not have. In
February 2023 **Toolformer**, by Timo Schick and colleagues, taught a model to decide for itself
which APIs to call, when, and with what arguments; its tools were a
calculator, a question-answering system, two search engines, a translator
and a calendar.

Products followed. On 13 June 2023 **[OpenAI](kloom:e/openai)** added _function calling_ to
its API: a developer describes functions, and the model replies with a JSON
object of arguments instead of prose. Every major lab soon offered the same
thing. On 22 October 2024 **[Anthropic](kloom:e/anthropic)** released _computer use_ in public
beta, letting [Claude](kloom:e/claude-ai) 3.5 Sonnet work a desktop from screenshots, moving the
pointer and typing. On the _OSWorld_ benchmark of computer tasks it scored
14.9%, against 7.8% for the next-best system. OpenAI's Computer-Using Agent,
behind its Operator preview of January 2025, reported 38.1%; the human score
on the same benchmark was 72.4%.

Each tool once needed its own integration. In November 2024 Anthropic
published the **[Model Context Protocol](kloom:e/model-context-protocol)** (MCP), an open standard for
connecting assistants to data and tools: one protocol, many servers, the
spokes of the drawing. By December 2025, Anthropic said, [ChatGPT](kloom:e/chatgpt), Gemini,
Microsoft Copilot and VS Code all used it, and that month Anthropic gave it to the **Agentic AI Foundation**, a new Linux
Foundation body whose founding projects also included Block's _goose_ and
OpenAI's _AGENTS.md_, and whose members included [Google](kloom:e/google), Microsoft and
OpenAI.

## Agents in the repository

Code suited agents: the work is text, and tests say whether it worked.
Cognition announced **Devin**, "the first AI software engineer", in March 2024. Anthropic's **Claude Code**, a terminal agent that reads code, edits
files, runs tests and commits, followed in February 2025; OpenAI's cloud
agent **Codex** in May 2025, with [GitHub](kloom:e/github)'s Copilot coding agent and Google's
**Jules** within days of it.

The yardstick was **SWE-bench** (October 2023), by **Carlos Jimenez** and
colleagues: 2,294 real
GitHub issues from 12 [Python](kloom:e/python-programming-language) projects. A model is given the repository and
the issue, and its patch counts only if the project's own tests pass. The
best model in the paper, Claude 2, solved 1.96%. In August 2024 OpenAI and
the benchmark's authors published **SWE-bench Verified**, 500 problems
checked by 93 developers, after finding tests that were too specific or
unrelated to the issue and descriptions too vague to act on.

| Reported | Model             | Lab       | SWE-bench Verified |
| -------- | ----------------- | --------- | -----------------: |
| Aug 2024 | GPT-4o            | OpenAI    |              33.2% |
| Oct 2024 | Claude 3.5 Sonnet | Anthropic |              49.0% |
| Feb 2025 | Claude 3.7 Sonnet | Anthropic |            63.7% ¹ |
| May 2025 | Claude Sonnet 4   | Anthropic |              72.7% |
| Aug 2025 | GPT-5             | OpenAI    |            74.9% ² |
| Sep 2025 | Claude Sonnet 4.5 | Anthropic |              77.2% |
| Nov 2025 | Gemini 3 Pro      | Google    |              76.2% |
| Feb 2026 | Claude Opus 4.6   | Anthropic |              80.8% |
| Jul 2026 | Claude Opus 5     | Anthropic |              96.0% |

These are the labs' own numbers at launch, each with its own scaffold and
number of trials. ¹ On 489 of the 500 problems. ² On 477 of them.

## What the score measures

SWE-bench measures one thing well: whether a patch makes a project's tests
pass, in Python, on issues whose fixes are public. It does not measure
whether the patch is good code, and it has leaked. A 2024 study, _SWE-Bench+_,
found the solution already given in the issue or its comments for 32.67% of
successful patches, and weak tests behind another 31.08%. In 2025 agents
were caught running `git log --all` and reading the future commit that fixed
the bug. In February 2026 OpenAI stopped reporting Verified at all: its
audit found flawed tests in at least 59.4% of the problems it checked, and
frontier models able to reproduce the original fixes from memory. It
recommended Scale AI's harder _SWE-bench Pro_ instead. Scores reported
since, like the last row above, come from a benchmark one lab has called
contaminated.

As of September 2026, then, the headline number says less than it seems to.
What it does record is real: in two years, models went from fixing almost
none of a set of real bugs to fixing most of them. The same years brought
models that think at length before they answer or act: reasoning models,
the next frame.
