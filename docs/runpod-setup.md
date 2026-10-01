# RunPod setup (modeOn)

## 1. Pod

- Template: **PyTorch 2.x + CUDA 12**
- GPU: **24 GB VRAM** (RTX 3090 / 4090 / A5000)
- Attach **Network Volume** (~50 GB) mounted at `/runpod-volume`

## 2. Clone & env

```bash
cd /runpod-volume
git clone <your-repo-url> modeOn
cd modeOn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install TTS==0.22.0 torch torchaudio
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

```bash
# Coqui CLI smoke test (adjust paths)
tts --text "Selamat pagi." \
  --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
  --speaker_wav /runpod-volume/voices/default/reference.wav \
  --language_idx ms \
  --out_path /runpod-volume/samples/test.wav
```

Generate samples from `tests/sentences_ms.txt` and log results in `docs/validation-week1.md`.

## 4. Run API

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

In RunPod: **Connect** → HTTP port **8000** (or TCP proxy).

## 5. Cost

Stop the pod when idle. Keep models and checkpoints on the network volume only.

Document the exact `pip` / `TTS` versions that worked in this file after first successful run.
