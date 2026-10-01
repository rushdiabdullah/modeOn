# RunPod setup (modeOn)

## 1. Pod

- Template: **PyTorch 2.x + CUDA 12**
- GPU: **24 GB VRAM** (RTX 3090 / 4090 / A5000)
- Attach **Network Volume** (~50 GB) mounted at `/runpod-volume`

## 2. Clone & env

```bash
cd /runpod-volume
git clone https://github.com/rushdiabdullah/modeOn.git modeOn
cd modeOn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-gpu.txt
# Or: ./scripts/runpod_bootstrap.sh
cp .env.example .env
```

Edit `.env`:

```env
API_KEY=<strong-secret>
MODEON_TTS_MODE=xtts
DEVICE=cuda
DEFAULT_SPEAKER_WAV=/runpod-volume/voices/default/reference.wav
```

Place a clean **6–30 s** (or longer) reference WAV at that path.

## 3. Validate (Week 1)

Full steps: **[week1-runbook.md](./week1-runbook.md)**

```bash
python scripts/week1_validate.py \
  --speaker-wav /runpod-volume/voices/default/reference.wav \
  --limit 10 \
  --output-dir /runpod-volume/samples/week1
```

Log listening scores in `docs/validation-week1.md` (use `samples/week1/scoring-template.md`).

## 4. Run API

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

In RunPod: **Connect** → HTTP port **8000** (or TCP proxy).

## 5. Cost

Stop the pod when idle. Keep models and checkpoints on the network volume only.

Document the exact `pip` / `TTS` versions that worked in this file after first successful run.
