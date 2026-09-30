In 1998 the software that [Richard Stallman](kloom:e/richard-stallman) called free was given a second
name, chosen to sound like a way of doing business rather than a cause.
Under that name it spread from hobbyists to the whole industry, until
almost every program anyone ships is built on code that strangers maintain
in public, sometimes one of them alone. What follows was true as of 28
September 2026.

## A name for a business case

On **22 January 1998** [Netscape](kloom:e/netscape) announced that it would give its Navigator browser away and publish the
source code of the next version of Communicator, under a licence it said
built on the heritage of the GNU GPL, to "harness the creative power of
thousands of programmers on the Internet". The code went out in March,
and became the Mozilla project.

A book-length argument for doing so was already circulating. In [_The
Cathedral and the Bazaar_](kloom:e/the-cathedral-and-the-bazaar), first given at the Linux Kongress in Würzburg
on 27 May 1997, **[Eric S. Raymond](kloom:e/eric-s-raymond)** contrasted two ways of building free
software: the _cathedral_, where a small group works in private between
releases (his examples were GNU Emacs and GCC), and the _bazaar_ of the
Linux kernel, developed in public over the Internet. Its thesis he named
Linus's law: "given enough eyeballs, all bugs are shallow."

On 3 February 1998, at a strategy session in Palo Alto called in the wake
of Netscape's announcement, the participants looked for a label that
would carry the business case without the politics of "free software".
**Christine Peterson** suggested [_open source_](kloom:e/open-source). Raymond and **Bruce
Perens** founded the **[Open Source Initiative](kloom:e/open-source-initiative)** that month (on 8 February
by one account; the OSI's own history says late February), and its _Open
Source Definition_ was Perens's _Debian Free Software Guidelines_ of 1997
with the Debian references taken out. The FSF kept its own word. Nearly all
free software is open source and nearly all open source is free, it says,
but the two names stand for different things: one a method, the other the
user's freedom.

## Tools for a bazaar

The web was already running on it. The **Apache** web server began in
early 1995 from patches to the stalled NCSA server, and it quickly overtook
NCSA's as the dominant web server. Its name has two stories: the project's 1995
documentation called it a pun on "a patchy server", while its foundation
later said it was chosen out of respect for Native Americans.

Working in public needs a way to merge the work of thousands. In April
2005 the Linux kernel lost the free use of BitKeeper, the proprietary
version-control system it had used since 2002, and **[Linus Torvalds](kloom:e/linus-torvalds)**
began writing [**git**](kloom:e/git) on 3 April. In git every copy of a project holds its
whole history, and every commit names its parent by a hash of its
contents, as the plate draws: a branch is a line of commits that leaves
the main one, and a merge is a commit with two parents. [**GitHub**](kloom:e/github),
launched in April 2008, put git repositories on the web, where anyone could
copy one into a _fork_ of their own and offer changes back. It had 100 million developers by January 2023; Microsoft bought
it for $7.5 billion in 2018; and in October 2025 it reported more than 180
million developers, 63% of whose repositories were public.

## The base of everything, and its cracks

In Black Duck's audits of 947 commercial codebases between November 2024
and October 2025, published in February 2026, 98% contained open-source
components. They held 581 known vulnerabilities on average, up from 280 a
year before, though the median codebase had 78. Much of that
base is maintained by very few people, and three failures showed what that
means.

| Year disclosed | Component | What went wrong                                              | Hidden for  |
| -------------- | --------- | ------------------------------------------------------------ | ----------- |
| 2014           | OpenSSL   | Heartbleed: a missing bounds check leaked server memory      | two years   |
| 2021           | Log4j     | Log4Shell: a logged string could load and run remote code    | eight years |
| 2024           | XZ Utils  | a backdoor planted by a trusted maintainer, reaching OpenSSH | weeks       |

[**Heartbleed**](kloom:e/heartbleed) (CVE-2014-0160) was in OpenSSL from its release of March
2012 until April 2014; at disclosure about 17% of the Internet's certified
secure web servers were believed vulnerable. OpenSSL was then maintained by a handful of volunteers, one of
them full time, on donations of about $2,000 a year. **Log4Shell**
(CVE-2021-44228), in a Java logging library, had been there since 2013
when Chen Zhaojun of Alibaba Cloud reported it on 24 November 2021; Apache
rated it 10, the highest severity. The [**xz** backdoor](kloom:e/xz-utils-backdoor) (CVE-2024-3094) was
patient. From 2021 an account called "Jia Tan" helped maintain the
compression library while sock puppets pressed its tired maintainer to
share the work; in February 2024 Jia Tan released versions carrying a
backdoor that, through a patch some distributions apply, reached the SSH
server. On 29 March 2024 **Andres Freund**, a developer at Microsoft,
reported it after noticing that SSH logins on a test system were using a
lot of CPU. It had not yet reached most production systems.

Open source is how software is now written. The next frame turns from the
software to a processor design that, like it, was licensed rather than
sold: ARM.
