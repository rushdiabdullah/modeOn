# modeOn — Roadmap (Solo + RunPod)

Malaysian Neural Voice API · XTTS v2 · FastAPI · MVP → Alpha

**Assumptions:** one person, no owned GPU yet, RunPod for all GPU work, budget ~RM300–800 for cloud before hardware decision.

---

## Outcomes by phase

| Phase | Duration | Done when |
|-------|----------|-----------|
| **0 — Validate** | Week 1 | XTTS runs on RunPod; 10 BM sentences sound acceptable to you |
| **1 — MVP API** | Weeks 2–3 | `POST /v1/tts` on RunPod returns WAV; API key; basic docs |
| **2 — Voice v1** | Week 4 | Boss/reference voice fine-tuned or strong zero-shot clone; 50-sentence QA |
| **3 — Alpha** | Weeks 5–8 | 1–3 friendly users; rate limit; simple monitoring |
| **4 — Decision** | End Week 8 | Go/no-go: buy server vs stay cloud vs pivot engine |

---

## RunPod setup (do once)

1. **Account:** [runpod.io](https://www.runpod.io) — add payment, set spend limit (e.g. USD 50–100).
2. **Pod template:** GPU **RTX 4090 24GB** or **A5000 24GB** (cheaper: **RTX 3090 24GB**). Community Cloud OK for dev.
3. **Image:** PyTorch 2.x + CUDA 12 (RunPod “PyTorch” templates work).
4. **Volume:** attach **Network Volume** (~50GB) for model weights + checkpoints (survives pod restarts).
5. **Access:** SSH or Jupyter; expose port **8000** for FastAPI (RunPod TCP proxy or custom domain later).
6. **Cost habit:** **stop pod** when not training; use volume so you don’t re-download models daily.

**Rough cost:** ~USD 0.30–0.70/hr active → ~RM300–500 if you run ~20–40 hrs over a month (validation + fine-tune + testing).

---

## Week 0 — Prep (local, no GPU)

**Goal:** repo + data plan before burning GPU hours.

- [ ] Create repo structure (see bottom of this doc).
- [ ] List **50 BM test sentences** (names, numbers, loanwords, short/long).
- [ ] Plan **reference voice:** 2–4 hours clean WAV (48kHz or 24kHz mono, no music/noise) OR accept 6–30 min for zero-shot clone only (lower quality).
- [ ] `.env.example`: `API_KEY`, `MODEL_PATH`, `DEFAULT_SPEAKER`.
- [ ] Read PDPA basics: consent if cloning someone’s voice; don’t ship without it.

**Deliverable:** `tests/sentences_ms.txt` + recording checklist.

---

## Week 1 — Validate (RunPod)

**Goal:** prove XTTS + BM is good enough to continue.

- [ ] Start pod with 24GB GPU + network volume.
- [ ] Install pinned stack (example):

  ```bash
  pip install TTS==0.22.0 torch torchaudio fastapi uvicorn python-multipart
  ```

  (Adjust version if install fails; document what worked in `docs/runpod-setup.md`.)

- [ ] Download XTTS v2; run **CLI inference** on 10 lines from `sentences_ms.txt`.
- [ ] Score honestly (1–5): clarity, BM pronunciation, naturalness.
- [ ] Measure **latency** for ~30-word sentence (target doc: &lt;2s on GPU — ok if 2–4s on first pass).

**Go/no-go gate:** average score ≥3.5 on clarity + you’d show this to one trusted listener. If &lt;3, spend 2 days trying **zero-shot with better reference clip** or note “need fine-tune / alt engine” before Week 2.

**Deliverable:** folder `samples/week1/` with WAVs + `docs/validation-week1.md` (scores + notes).

---

## Week 2 — FastAPI skeleton (RunPod)

**Goal:** one documented HTTP API.

- [ ] `POST /v1/tts` body:

  ```json
  {"text": "...", "speaker_id": "default", "language": "ms", "speed": 1.0}
  ```

- [ ] Response: `audio/wav`, 24 kHz (match XTTS output).
- [ ] Header: `X-API-Key` (reject if missing/wrong).
- [ ] Swagger at `/docs`.
- [ ] Wrap model load **once at startup** (not per request).
- [ ] Max text length (e.g. 500 chars) to avoid abuse.

**Deliverable:** curl example in README; pod URL + API key for your own tests only.

---

## Week 3 — Harden MVP

**Goal:** stable enough for daily use; not production-scale yet.

- [ ] Health: `GET /health` (GPU ok, model loaded).
- [ ] Error responses: empty text, timeout, OOM → clear JSON.
- [ ] Optional: **Redis-less** file cache — hash `(text, speaker_id, speed)` → reuse WAV (big latency win for repeats).
- [ ] Dockerize (`docker/Dockerfile`) so same image runs on RunPod or future bare metal.
- [ ] Simple load test: 10 sequential requests; note p95 latency.

**Deliverable:** `docker compose up` works on pod; tag image in RunPod or Docker Hub (private).

---

## Week 4 — Voice v1 (Boss / reference)

**Goal:** default speaker sounds like *your* product, not generic XTTS.

**Path A — Zero-shot (faster, solo-friendly):** 6–30 s clean reference + `speaker_id` / conditioning wav (XTTS flow). Good for demo; weaker for brand voice.

**Path B — Fine-tune (doc Phase 1):** 30–60 min minimum, **2–4 hr recommended**; QLoRA/full per your GPU time budget.

- [ ] Normalize audio (trim silence, consistent levels).
- [ ] Fine-tune on RunPod (longest GPU block this month — schedule 4–8 hr session).
- [ ] Run **50-sentence QA**; log failures (numbers, English words in BM, names).
- [ ] Start **glossary** (`data/glossary.txt`): company names, product terms → preferred spelling in text input.

**Deliverable:** checkpoint on network volume + `speakers/default` config; QA sheet in `docs/voice-v1-qa.md`.

---

## Weeks 5–6 — Alpha prep

**Goal:** safe sharing with 1–3 businesses.

- [ ] `GET /v1/speakers` — list `default` (+ any others).
- [ ] Rate limit: e.g. 100 req/day per API key (in-memory OK for alpha; Redis later).
- [ ] Request logging: timestamp, chars, duration ms (no full text if sensitive — or hash text).
- [ ] Terms: “alpha, no SLA”; API key rotation procedure.
- [ ] One-page **integration guide** (curl + Python `requests`).

**Deliverable:** 2 alpha keys; shared Notion/PDF guide.

---

## Weeks 7–8 — Alpha run + learn

**Goal:** real feedback, minimal scope creep.

- [ ] Onboard **1–3** friendly users (e-learning, podcast, small call flow — pick one vertical).
- [ ] Weekly: collect bad samples → fix glossary or text preprocessing.
- [ ] Track: requests/day, error rate, p95 latency, $ RunPod spend.
- [ ] **Decision meeting (with yourself):**
  - **Buy server** if spend predictable & quality OK.
  - **Stay RunPod** if usage spiky or still iterating.
  - **Pivot engine** if BM blockers remain after glossary + fine-tune.

**Deliverable:** `docs/alpha-retro.md` + decision recorded.

---

## After Week 8 (only if go)

Pick **one** track; don’t do all solo at once.

| Track | Focus |
|-------|--------|
| **Commercial** | Pricing draft, invoice, 1 paid pilot |
| **Product** | `/v1/clone` upload (consent flow), second speaker |
| **Ops** | Queue (Redis + worker), streaming TTS |
| **Hardware** | RTX 3090 build; migrate volume → local Docker |

---

## Solo rules (avoid burnout)

1. **GPU hours:** batch training; stop pod overnight.
2. **Scope:** one endpoint, one default voice until alpha feedback.
3. **Quality:** fix with **text** (glossary, normalization) before re-training.
4. **Security:** never commit API keys; alpha keys per client.
5. **Legal:** written consent before cloning anyone’s voice.

---

## Suggested repo layout

```text
modeOn/
├── ROADMAP.md                 # this file
├── README.md
├── .env.example
├── api/
│   ├── main.py
│   ├── auth.py
│   └── routes/
│       └── tts.py
├── tts/
│   ├── engine.py              # XTTS load + synthesize
│   └── config.py
├── data/
│   ├── glossary.txt
│   └── recordings/            # gitignore raw voice
├── tests/
│   └── sentences_ms.txt
├── samples/                   # gitignore generated wav
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── docs/
    ├── runpod-setup.md
    ├── validation-week1.md
    └── voice-v1-qa.md
```

---

## Quick reference — Week 1 checklist (print this)

```
[ ] RunPod account + spend cap
[ ] Network volume mounted
[ ] Pod 24GB GPU running
[ ] XTTS inference works
[ ] 10 BM WAVs generated
[ ] Latency noted
[ ] Go/no-go written
[ ] Pod STOPPED
```

---

## Success metrics (MVP)

| Metric | Target (alpha) |
|--------|----------------|
| Latency (30 words, GPU) | &lt; 3 s p95 |
| Uptime | best effort (alpha) |
| BM QA pass rate | ≥ 80% on 50-sentence set |
| RunPod spend | within monthly cap you set |

---

*Last updated: 2026-10-01 · Solo + RunPod track*
