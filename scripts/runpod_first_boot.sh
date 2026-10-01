#!/usr/bin/env bash
# Optional: run once on a new pod after Web Terminal opens (or from cron @reboot).
set -euo pipefail
LOG="${MODEON_BOOT_LOG:-/workspace/modeon_boot.log}"
exec > >(tee -a "$LOG") 2>&1
echo "==> modeOn first boot $(date -u +%Y-%m-%dT%H:%M:%SZ)"

export RUNPOD_VOLUME="${RUNPOD_VOLUME:-/workspace}"
cd "$RUNPOD_VOLUME"

if [[ -x modeOn/scripts/runpod_bootstrap.sh ]]; then
  cd modeOn && git pull --ff-only || true
else
  git clone "${MODEON_REPO:-https://github.com/rushdiabdullah/modeOn.git}" modeOn
  cd modeOn
  chmod +x scripts/runpod_bootstrap.sh
fi

./scripts/runpod_bootstrap.sh

REF="${RUNPOD_VOLUME}/voices/default/reference.wav"
if [[ -f "$REF" ]]; then
  source .venv/bin/activate
  python3 scripts/week1_validate.py \
    --speaker-wav "$REF" \
    --limit 10 \
    --output-dir "${RUNPOD_VOLUME}/samples/week1"
  echo "==> Week 1 validate done"
else
  echo "==> SKIP week1_validate — upload reference.wav to ${REF} then re-run this script"
fi
