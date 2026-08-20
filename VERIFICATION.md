# SECPQUEST v0.1 Verification

Owner: **Telegram @intelwire**

Verified locally on 2026-08-20.

## Tests

- 10/10 Python unit tests passed.
- secp256k1 generator and curve-order identities passed.
- known private scalar `1` maps to Bitcoin address `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH`.
- compressed public-key round trip passed.
- WIF encode/decode round trip passed.
- DER ECDSA R/S parser regression test passed.
- deterministic shard coverage test passed with no gaps/overlaps.
- synthetic 20-bit challenge candidate verification passed.
- real incremental scanner found the synthetic key `0xabcde` from a nearby start after 15 checks.
- Web server `/`, `/api/puzzles`, and `/api/verify` were exercised over HTTP and returned HTTP 200 / correct results.

## Public challenge manifests

Bitcoin Puzzle #71 metadata was checked against the public BTC Puzzle listing on 2026-08-20. Puzzles #72 and #73 were also sourced from the same current public listing. These statuses can change; always re-check upstream before allocating compute.

## Important performance note

The scanner is a correct pure-Python CPU reference implementation. It is not presented as competitive for 70+ bit public puzzles. There is no fake GPU speed, no hidden demo success path, and no claim that parity or address patterns reveal unknown key bits.
