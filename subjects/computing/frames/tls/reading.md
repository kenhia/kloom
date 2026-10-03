Nothing in the layers below keeps a secret. An Ethernet frame is heard by
every station on its segment, an IP packet can be read by every router it
crosses, and a DNS answer can be forged. [Transport Layer Security](kloom:e/transport-layer-security) wraps a
TCP connection so that it proves who is at the other end, encrypts
everything in between, and detects any tampering. Its tools are [public-key
cryptography](kloom:e/public-key-cryptography), invented in the 1970s, and certificates. This frame describes
TLS as it stood on 28 September 2026.

## From Netscape's layer to the IETF's

It began as a product feature. [Netscape Communications](kloom:e/netscape) created HTTPS in
1994 for its Navigator browser, carried over its own _Secure Sockets
Layer_, whose design is credited to its chief scientist **[Taher Elgamal](kloom:e/taher-elgamal)**.
Version 1.0 was never released. Version 2.0, shipped in February 1995, had serious flaws:
it used the same keys for encryption and for authenticating messages, and
nothing protected the opening handshake from an attacker in the middle.
**Paul Kocher**, with Netscape's **Phil Karlton** and **Alan Freier**,
redesigned it as SSL 3.0 in 1996, and every later version descends from
that one.

The IETF took it over and renamed it. **Tim Dierks** and **Christopher
Allen** wrote TLS 1.0, RFC 2246, in January 1999. Its differences from SSL
3.0 were, the RFC says, "not dramatic" but enough to stop the two
interoperating; Dierks later described the new name, as Wikipedia quotes
him, as a face-saving gesture to Microsoft.

| Version | Published | Retired                        |
| ------- | --------- | ------------------------------ |
| SSL 2.0 | 1995      | 2011 (RFC 6176)                |
| SSL 3.0 | 1996      | 2015, after the POODLE attack  |
| TLS 1.0 | 1999      | 2021 (RFC 8996)                |
| TLS 1.1 | 2006      | 2021 (RFC 8996)                |
| TLS 1.2 | 2008      | in use; no retirement date set |
| TLS 1.3 | 2018      | current; revised in July 2026  |

TLS 1.3, RFC 8446 of August 2018, was a clean-up: weak and obsolete
options removed, fresh keys required for every session, so that a stolen
server key cannot unlock recordings of old ones, and a handshake one round
trip long. RFC 9846, published in July 2026, replaced both it and the TLS
1.2 specification with a single revised text.

## Who you are talking to

Encryption with a stranger is no use if the stranger is an impostor. A
_certificate_ binds a name, such as `example.org`, to a public key, and is
signed by a [_certificate authority_](kloom:e/certificate-authority). The plate draws the chain a browser
checks: the site's certificate is signed by an intermediate authority,
whose certificate is signed by a root authority, whose key the browser or
operating system already holds in its trust store. The site proves it
holds the private key that matches its certificate, and the handshake
derives fresh keys for the session.

For twenty years certificates cost money and effort, and most sites did
without. **[Let's Encrypt](kloom:e/lets-encrypt)**, begun in 2012 by **Josh Aas** and **Eric
Rescorla** of Mozilla, **Peter Eckersley** of the Electronic Frontier
Foundation and **J. Alex Halderman** of the University of Michigan, gave
them away. It issued its first certificate on 14 September 2015 and opened
to the public that December. A program on the web server proves control of
the domain through a protocol called ACME, then fetches and renews a
certificate valid for 90 days, with no one involved. On 27 September 2026
it issued 6.9 million certificates, and 692 million were active, covering
231 million registered domains.

## How much is encrypted

![Bar chart: the share of Firefox page loads made over HTTPS each September rose from 32 per cent in 2014 to 62 in 2017 and 84 in 2020, and has stayed between 81 and 86 since](https-share.svg)

| September       | 2014 | 2016 | 2017 | 2018 | 2020 | 2022 | 2024 | 2025 | 2026 |
| --------------- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Firefox HTTPS % |   32 |   46 |   62 |   75 |   84 |   82 |   82 |   86 |   81 |

The two big browsers measure it differently and disagree. Firefox's
telemetry, which Let's Encrypt publishes, has hovered in the low to middle
80s since 2020. Chrome's security team reported in October 2025 that
HTTPS had risen from 30–45 per cent of Chrome's page loads in 2015 to
95–99 per cent by about 2020, after which progress "largely plateaued". Part of the gap is private
sites: counting only public ones, Chrome on Linux rose from 84 to nearly 97
per cent. From version 154, in October 2026, Chrome planned to ask every
user's permission before first loading any public site without HTTPS.

## Against a future computer

A recording of encrypted traffic can be kept for decades. If a large
[quantum computer](kloom:e/quantum-computing) is ever built, [Shor's algorithm](kloom:e/shors-algorithm) would recover the keys
from today's key exchanges, so an attacker can harvest now and decrypt
later. The answer is already deployed. NIST standardized [**ML-KEM**](kloom:e/ml-kem), a key
exchange based on lattice problems, as FIPS 203 in August 2024, and TLS 1.3
now runs it alongside the classical exchange, X25519, so the session stays
safe while either one holds; the plate draws the two feeding one key
derivation. Chrome turned the hybrid on by default in November 2024, and
Firefox in version 132. Cloudflare reported in April 2026 that over 65 per
cent of human traffic to its network was post-quantum encrypted. The
certificates are not yet: post-quantum signatures are larger, and
Cloudflare set 2029 as its target for finishing the change.

Five layers, each doing one job and trusting nothing from the others: a
cable shared by taking turns, an address on every packet, a stream made
out of losses, a tree of names, and a sealed envelope over all of it. That
division of labor is what the internetworking design of the 1970s
promised; this trail began at TCP/IP.
