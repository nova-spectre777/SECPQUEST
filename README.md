<div align="center">

# SECPQUEST
### RANGE-Ω · Public Bitcoin Puzzle Mathematics & Verifiable Search Engine

**CLI + Web · secp256k1 · range search · puzzle manifests · proof-of-search receipts**

Owner: **Telegram [@intelwire](https://t.me/intelwire)**

</div>

SECPQUEST is a math-first toolkit for explicit **public Bitcoin puzzle challenges** and synthetic secp256k1 exercises. It is not a generic wallet-targeting or private-key recovery suite. Search is allowlisted to manifests shipped in `manifests/` with `kind=public_challenge` or `kind=synthetic`.

## CLI

```bash
python -m secpquest.cli list-puzzles
python -m secpquest.cli show bitcoin-puzzle-71
python -m secpquest.cli plan bitcoin-puzzle-71 --shards 1024 --index 17
python -m secpquest.cli point 0x12345
python -m secpquest.cli verify synthetic-20 0xabcde
python -m secpquest.cli search synthetic-20 --max-keys 600000
```

## Web

```bash
python -m secpquest.cli web
# open http://127.0.0.1:8787
```

No external Python package is required.

## What RANGE-Ω does

1. Loads an approved challenge manifest.
2. Represents the scalar interval exactly.
3. Partitions it deterministically into non-overlapping shards.
4. Uses incremental secp256k1 point addition for the CPU reference scanner.
5. Verifies compressed and uncompressed P2PKH candidates.
6. Emits checkpoint hashes and a Merkle-style work root for reproducible receipts.
7. Reports actual measured throughput rather than fake ETA claims.

**Reality check:** the pure-Python scanner is a correctness/reference engine, not a competitive GPU implementation for 70+ bit puzzles.

See `docs/FEATURE_MATRIX.md`, `docs/ALGORITHM.md`, and `docs/SAFETY.md`.
