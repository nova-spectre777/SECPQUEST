# Safety boundary

Owner: Telegram @intelwire

SECPQUEST intentionally separates puzzle mathematics from generic wallet cracking.

- Search runs only for built-in manifests marked `public_challenge` or `synthetic`.
- No command accepts an arbitrary Bitcoin address as a private-key search target.
- Blockchain/transaction tooling is read-only analysis.
- R-reuse/nonce modules are detection/statistics in the generic path; they do not recover arbitrary wallet keys.
- No seed-phrase cracking, wallet.dat password brute force, key-draining, transaction broadcast, or arbitrary-target GPU cracker is included.
- Public challenge metadata can become stale; verify the challenge source before spending compute.
