IP delivers packets when it can. Programs want something else: a
conversation, a file or a web page that arrives complete, in order and
exactly once. The Transmission Control Protocol builds that out of IP's
unreliable packets, using nothing but the two computers at the ends. It
does it with numbers, a timer and, since 1988, a sense of when to slow down.

## A number on every byte

TCP's first specification, **RFC 675** of December 1974 by **Vint Cerf**,
**Yogen Dalal** and **Carl Sunshine**, described one program that did
everything; the version standardised as **RFC 793** in September 1981 left
addressing and routing to IP. Its method takes a few sentences of RFC 793.
Every byte sent is given a _sequence number_. The receiver sends back an
_acknowledgement_ naming the next byte it expects, which confirms everything
before it. A sender that hears no acknowledgement within a timeout sends
the data again. The receiver uses the numbers to put segments back in
order and to throw away duplicates, a checksum on every segment catches
damage, and a _window_ in each acknowledgement tells the sender how much
more it may send.

Before any data flows, the two ends agree on where their numbering starts,
and each confirms the other's. That is the **three-way handshake**, drawn in
the plate with RFC 793's own example numbers:

| Step | Segment                          | A's state   | B's state    |
| ---: | -------------------------------- | ----------- | ------------ |
|    1 | A → B: SYN, seq 100              | SYN-SENT    | LISTEN       |
|    2 | B → A: SYN+ACK, seq 300, ack 101 | ESTABLISHED | SYN-RECEIVED |
|    3 | A → B: ACK, seq 101, ack 301     | ESTABLISHED | ESTABLISHED  |

Each side starts from its own number rather than zero so that a stray
segment from an old connection cannot be mistaken for part of a new one.
RFC 793 took the starting number from a 32-bit clock ticking about every
four microseconds, which wraps round every 4.55 hours, longer than a
segment was expected to survive in the network. After the handshake, the
plate loses a data segment: no acknowledgement comes, the timer runs out,
and A sends the same bytes again.

## Collapse

Retransmission has a danger in it. When a router's queue overflows it drops
packets, senders time out and send again, and the extra traffic makes the
queues longer still. In October 1986 the Internet had the first of what
became a series of _congestion collapses_: between Lawrence Berkeley
Laboratory and the University of California at Berkeley, 400 yards and two
IMP hops apart, throughput fell from 32 kbit/s to 40 bit/s, a factor of
about a thousand.

**Van Jacobson** of LBL and **Michael Karels** of Berkeley traced the
fault to how TCP was implemented, not to the protocol, and by 1988 had put
seven new algorithms into Berkeley Unix's TCP. Their principle was
_conservation of packets_: a connection in equilibrium should put a new
packet into the network only as an old one leaves. Two rules did most of the
work, both governed by a _congestion window_ that caps how much a sender
has in flight:

| Rule                 | What the sender does                                   |
| -------------------- | ------------------------------------------------------ |
| Slow start           | begin at one packet; add one for every acknowledgement |
| Congestion avoidance | on a timeout, halve the window                         |
|                      | otherwise, grow by about one packet per round trip     |

Slow start, despite its name, doubles the window every round trip until it
finds the path's limit. The halving and the slow growth after it are
_additive increase, multiplicative decrease_, a policy the paper takes
from **Raj Jain**, K. K. Ramakrishnan and Dah-Ming Chiu at Digital
Equipment. Jacobson and Karels also noted that slow start closely
resembles Jain's CUTE, which had preceded it by several months without
their knowing.

## The ends decide

Why put all this in the hosts rather than the network? **Jerome Saltzer**,
**David Reed** and **David Clark** of MIT's Laboratory for Computer Science
gave the reason a name in 1981,
published in its best-known form in 1984: the _end-to-end argument_. A
function, they wrote, "can completely and correctly be implemented only with
the knowledge and help of the application standing at the end points of the
communication system." Their example is a careful file transfer: however
reliable each link, the file can still be damaged on a disk or in a
program's memory, so only a check made by the application at the far end
proves it arrived intact. Checks in the network help performance; they
cannot replace that one. IP's plainness and TCP's place at the ends are
that argument built.

TCP has kept evolving at the ends. In August 2022 **RFC 9293** gathered
four decades of amendments into one document and retired RFC 793. Linux
has used a newer congestion rule, CUBIC, by default since 2006, and Google
introduced BBR, which models the path instead of waiting for losses, in 2016. **QUIC**, standardised in May 2021, rebuilds reliable streams on top
of UDP with encryption built in, and HTTP/3 runs over it. A reliable
connection still needs an address to connect to, and people remember names
instead, which is the next layer's work.
