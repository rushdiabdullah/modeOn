# modeOn

Self-hosted Malaysian neural voice API (XTTS v2 + FastAPI). See [ROADMAP.md](./ROADMAP.md) for solo + RunPod plan.

## Quick start (local, mock TTS)

```bash
python3.11 -m venv .venv   # 3.10+ recommended; RunPod uses 3.11
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env — set API_KEY

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger: http://localhost:8000/docs  
- Health: http://localhost:8000/health  

## Try TTS

```bash
curl -sS -X POST http://localhost:8000/v1/tts \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"Selamat pagi, ini ujian suara.","speaker_id":"default","language":"ms","speed":1.0}' \
  --output out.wav
```

## Week 1 (RunPod validation)

Follow **[docs/week1-runbook.md](./docs/week1-runbook.md)** — bootstrap pod, generate 10 BM samples, go/no-go.

**Engine A/B:** **[docs/engine-compare.md](./docs/engine-compare.md)** — XTTS vs **F5-TTS** (`scripts/week1_validate_f5.py`).

## RunPod (API)

1. Set `MODEON_TTS_MODE=xtts` and install GPU deps (see [docs/runpod-setup.md](./docs/runpod-setup.md)).
2. Mount network volume; point `DEFAULT_SPEAKER_WAV` at your reference clip.
3. Run with Docker or `uvicorn` on port **8000**.

## Layout

```
api/          FastAPI app, auth, routes
tts/          XTTS engine wrapper
tests/        BM sentence list for QA
docker/       Container definitions
docs/         RunPod + validation notes
```

## License

Private / TBD.
