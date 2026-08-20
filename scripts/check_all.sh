#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT"
python -m unittest discover -s tests -v
python -m secpquest.cli list-puzzles >/dev/null
python -m secpquest.cli features >/dev/null
python -m secpquest.cli point 1 >/dev/null
python -m secpquest.cli verify synthetic-20 0xabcde >/dev/null
python -m secpquest.cli search synthetic-20 --start 0xabcd0 --max-keys 32 >/dev/null
echo 'SECPQUEST verification passed.'
