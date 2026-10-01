#!/usr/bin/env bash
# Run ONLY inside a RunPod pod terminal (GPU), not on your Mac.
set -euo pipefail

REPO_URL="${MODEON_REPO_URL:-https://github.com/rushdiabdullah/modeOn.git}"

detect_volume() {
  if [[ -n "${RUNPOD_VOLUME:-}" && -d "${RUNPOD_VOLUME}" ]]; then
    echo "${RUNPOD_VOLUME}"
    return 0
  fi
  for candidate in /runpod-volume /workspace; do
    if [[ -d "${candidate}" ]]; then
      echo "${candidate}"
      return 0
    fi
  done
  return 1
}

if ! VOL="$(detect_volume)"; then
  echo "ERROR: No RunPod data directory found (/runpod-volume or /workspace)."
  echo ""
  echo "This script must run on a RunPod pod (Web Terminal or SSH), not on your Mac."
  echo "  1. Deploy a GPU pod at runpod.io"
  echo "  2. Connect → Start Web Terminal"
  echo "  3. Optional: attach Network Volume (often mounts at /runpod-volume)"
  echo "  4. Or set: export RUNPOD_VOLUME=/path/shown/in/runpod/connect"
  echo ""
  if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "You appear to be on macOS — open the pod terminal in the browser instead."
  fi
  exit 1
fi

APP_DIR="${MODEON_APP_DIR:-${VOL}/modeOn}"

echo "==> modeOn bootstrap"
echo "    volume: ${VOL}"
echo "    app:    ${APP_DIR}"

mkdir -p "${VOL}/voices/default" "${VOL}/samples/week1"

if [[ ! -d "${APP_DIR}/.git" ]]; then
  git clone "${REPO_URL}" "${APP_DIR}"
else
  echo "==> repo exists, pulling latest"
  git -C "${APP_DIR}" pull --ff-only || true
fi

cd "${APP_DIR}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found on this pod. Use a PyTorch template image."
  exit 1
fi

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python3 -m pip install -U pip wheel
pip install -r requirements.txt
pip install -r requirements-gpu.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "==> created .env — set API_KEY and DEFAULT_SPEAKER_WAV when you run the API"
fi

REF="${VOL}/voices/default/reference.wav"
if [[ ! -f "${REF}" ]]; then
  echo ""
  echo "WARNING: missing reference voice: ${REF}"
  echo "Upload reference.wav before week1_validate.py (scp or RunPod file upload)."
  echo "See docs/recording-checklist.md"
  echo ""
fi

echo "==> done. Next (still on the POD):"
echo "  source ${APP_DIR}/.venv/bin/activate"
echo "  cd ${APP_DIR}"
echo "  python3 scripts/week1_validate.py --speaker-wav ${REF} --limit 10 --output-dir ${VOL}/samples/week1"
