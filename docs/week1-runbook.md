# Week 1 runbook — Validate XTTS + BM (RunPod)

**Goal:** 10 BM WAVs, latency numbers, go/no-go before Week 2.

**Time on GPU:** ~1–2 hours (install + first model download + 10 samples). **Stop the pod** when done.

> **Important:** Run bootstrap and `week1_validate.py` in the **RunPod pod terminal** (browser Web Terminal or SSH).  
> **Not** in Terminal.app on your Mac — `/runpod-volume` does not exist on macOS.

---

## Step 1 — RunPod console

1. Log in at [runpod.io](https://www.runpod.io).
2. **Storage → Network Volumes** → Create (~50 GB), note the mount path (usually `/runpod-volume`).
3. **Pods → Deploy**:
   - Template: **RunPod PyTorch 2.x** (CUDA 12)
   - GPU: **24 GB** (RTX 3090 / 4090 / A5000)
   - Attach your network volume
   - Container disk: 20 GB+ (temp/cache)
4. Start pod → **Connect** → **Start Web Terminal** (or SSH).

Set a **spend limit** in billing if you haven't already.

---

## Step 2 — Reference voice (before GPU work)

On your Mac, record or export **one clean WAV** (6–30 seconds minimum for zero-shot):

- Mono, 24 kHz or 48 kHz
- See [recording-checklist.md](./recording-checklist.md)

Upload to the volume:

```bash
# From Mac (replace POD_SSH with RunPod SSH command from Connect tab)
scp /path/to/reference.wav root@POD_SSH:/runpod-volume/voices/default/reference.wav
```

Or use RunPod file browser / Jupyter upload to `/runpod-volume/voices/default/reference.wav`.

---

## Step 3 — Bootstrap project on the pod

In the **pod** terminal, find where data lives:

```bash
ls -d /runpod-volume /workspace 2>/dev/null
```

Use whichever exists (network volume → usually `/runpod-volume`; else `/workspace`):

```bash
export RUNPOD_VOLUME=/runpod-volume   # or /workspace
cd "${RUNPOD_VOLUME}"
git clone https://github.com/rushdiabdullah/modeOn.git
cd modeOn
git pull origin main
chmod +x scripts/runpod_bootstrap.sh
./scripts/runpod_bootstrap.sh
```

Then:

```bash
source .venv/bin/activate
python3 scripts/week1_validate.py \
  --speaker-wav "${RUNPOD_VOLUME}/voices/default/reference.wav" \
  --limit 10 \
  --output-dir "${RUNPOD_VOLUME}/samples/week1"
```

Edit env (optional for Week 1 script; needed later for API):

```bash
nano /runpod-volume/modeOn/.env
# DEFAULT_SPEAKER_WAV=/runpod-volume/voices/default/reference.wav
```

---

## Step 4 — Run validation (10 sentences)

```bash
cd /runpod-volume/modeOn
source .venv/bin/activate

python scripts/week1_validate.py \
  --speaker-wav /runpod-volume/voices/default/reference.wav \
  --limit 10 \
  --output-dir /runpod-volume/samples/week1
```

Outputs:

- `/runpod-volume/samples/week1/01.wav` … `10.wav`
- `manifest.json` (latency stats)
- `scoring-template.md` (fill while listening)

**Download WAVs to your Mac** (SCP zip or RunPod file manager) and listen with headphones.

---

## Step 5 — Score & go/no-go

1. Open `samples/week1/scoring-template.md` (or copy into [validation-week1.md](./validation-week1.md)).
2. Rate each clip: **Clarity**, **BM**, **Natural** (1–5).
3. Check `manifest.json` → `summary.latency_30w_ref_s` (target &lt; 3 s ok for alpha; doc ideal &lt; 2 s).

| Result | Action |
|--------|--------|
| Clarity avg **≥ 3.5**, acceptable to show someone | **Go** → Week 2 on same pod |
| Clarity **&lt; 3** | Better reference WAV, retry; consider longer clip or fine-tune plan |
| BM weak but clarity ok | Continue with glossary + more reference data; note in validation doc |
| OOM / install fail | Try smaller batch, 3090 24GB, or pin different `TTS` version in `requirements-gpu.txt` |

Document versions that worked in [runpod-setup.md](./runpod-setup.md):

```bash
source .venv/bin/activate
pip freeze | grep -E '^(TTS|torch|torchaudio)=='
```

---

## Step 6 — Stop pod

**Pods → Stop** (keep network volume). Model cache on volume saves re-download next session.

---

## Optional — smoke test API on pod (preview Week 2)

```bash
cd /runpod-volume/modeOn
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
export MODEON_TTS_MODE=xtts
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

RunPod **Connect** → add HTTP port 8000 → test `/health` and `/docs`.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `CUDA out of memory` | Close other GPU processes; use 24GB GPU; one synthesis at a time |
| `speaker wav not found` | Path must match uploaded file exactly |
| Very slow first run | Normal — model download; later runs faster |
| `TTS` install fails | Use PyTorch template pod; `pip install TTS==0.22.0` only after torch |

---

## Week 1 checklist

```
[ ] Network volume created
[ ] Pod 24GB GPU ran bootstrap
[ ] reference.wav on volume
[ ] week1_validate.py completed (10 WAVs + manifest.json)
[ ] Listening scores recorded
[ ] Go/no-go decided
[ ] Pod STOPPED
[ ] pip versions noted in runpod-setup.md
```
