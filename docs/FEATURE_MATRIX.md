# CryptographyTube feature mapping → SECPQUEST

Source inspiration: `Cryptographytube/Cryptographytubetools` `index.html`. We reimplemented concepts, not code or branding.

## Implemented directly
- private scalar → public key / P2PKH / P2WPKH
- public key → X/Y coordinates + compressed/uncompressed forms
- HASH160 → P2PKH/P2SH/P2WPKH
- redeem/witness script → P2SH/P2WSH
- WIF encode/decode
- SHA256, double-SHA256, RIPEMD160, HASH160
- Base58Check primitives
- modular inverse over secp256k1 order
- elliptic-curve point multiplication
- raw transaction decoder
- DER R/S parser
- range planning, parity/range mathematics, deterministic sharding
- public-puzzle candidate verification
- real bounded CPU range search with incremental point addition
- proof-of-search checkpoint/work-root receipts
- CLI and browser UI over the same Python core

## Puzzle-lab / defensive equivalents
The source page includes generic key-recovery or exploit tools for R reuse, nonce bias/HNP, linear/inverse/circular nonces, signature faults, BIP32 leakage, invalid-curve fragments, SIGHASH anomalies, and bit leaks. SECPQUEST keeps these as puzzle/synthetic research or detection-only concepts; it does not expose arbitrary-wallet key extraction.

## Not copied as offensive/generic recovery
- arbitrary-address private-key recovery
- wallet.dat password cracking / passphrase brute force
- arbitrary BIP32 master-key extraction
- generic transaction mutation for malleability abuse
- arbitrary private-key consolidation/signing workflows
- seed phrase dumping/cracking

## UI concepts retained
- searchable categorized tools
- responsive web interface
- exportable JSON/text results
- transparent math explanations
- owner identity shown as Telegram @intelwire
