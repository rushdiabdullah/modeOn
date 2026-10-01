#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv-f5
# shellcheck disable=SC1091
source .venv-f5/bin/activate
pip install -U pip wheel
pip install -r requirements-f5.txt
echo "==> F5 venv ready. Edit data/reference_transcript.txt then run week1_validate_f5.py"
