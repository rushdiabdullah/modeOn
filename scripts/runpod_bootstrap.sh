#!/usr/bin/env bash
# One-time / repeat setup on a RunPod pod with network volume at /runpod-volume
set -euo pipefail

VOL="${RUNPOD_VOLUME:-/runpod-volume}"
REPO_URL="${MODEON_REPO_URL:-https://github.com/rushdiabdullah/modeOn.git}"
APP_DIR="${VOL}/modeOn"

echo "==> modeOn bootstrap (volume: ${VOL})"

if [[ ! -d "${VOL}" ]]; then
  echo "ERROR: ${VOL} not found. Attach a network volume or set RUNPOD_VOLUME."
  exit 1
fi

mkdir -p "${VOL}/voices/default" "${VOL}/samples/week1"

if [[ ! -d "${APP_DIR}/.git" ]]; then
  git clone "${REPO_URL}" "${APP_DIR}"
else
  echo "==> repo exists, pulling latest"
  git -C "${APP_DIR}" pull --ff-only
fi

cd "${APP_DIR}"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -U pip wheel
pip install -r requirements.txt
pip install -r requirements-gpu.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "==> created .env from .env.example — edit API_KEY and DEFAULT_SPEAKER_WAV"
fi

REF="${VOL}/voices/default/reference.wav"
if [[ ! -f "${REF}" ]]; then
  echo ""
  echo "WARNING: missing reference voice: ${REF}"
  echo "Upload a clean 6–30 s WAV before running week1_validate.py"
  echo "See docs/recording-checklist.md"
  echo ""
fi

echo "==> done. Next:"
echo "  source ${APP_DIR}/.venv/bin/activate"
echo "  cd ${APP_DIR}"
echo "  python scripts/week1_validate.py --speaker-wav ${REF}"
