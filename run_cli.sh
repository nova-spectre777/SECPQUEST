#!/usr/bin/env bash
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$ROOT"
exec python -m secpquest.cli "$@"
