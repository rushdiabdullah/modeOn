# Engine compare — XTTS vs F5-TTS (Week 1b)

Same inputs for a fair A/B test:

| Input | Path |
|-------|------|
| Reference audio | `/workspace/voices/default/reference.wav` |
| Reference transcript (F5 only) | `data/reference_transcript.txt` |
| Test sentences | `tests/sentences_ms.txt` (first 10) |

Outputs:

| Engine | Folder |
|--------|--------|
| Coqui XTTS v2 | `samples/week1/` |
| F5-TTS | `samples/week1-f5/` |

## Why F5-TTS as alternative?

- **pip install** on RunPod (no full Fish-Speech repo)
- Uses **reference WAV + exact transcript** (often less “random English prosody” than XTTS `language=en` hack)
- Not BM-specific either — compare by **listening**, not specs

Other engines later: Fish Speech (heavier setup), GPT-SoVITS, Piper (no clone).

---

## RunPod steps

1. **Start** pod `modeon-week1` (or new pod, 24GB GPU).
2. **XTTS** (if not done): existing `.venv` + `week1_validate.py` → `samples/week1/`.
3. **F5** — separate venv (avoids dependency fights):

```bash
cd /workspace/modeOn
git pull origin main

python3 -m venv .venv-f5
source .venv-f5/bin/activate
pip install -U pip wheel
pip install -r requirements-f5.txt
apt-get update && apt-get install -y portaudio19-dev libsox-dev ffmpeg 2>/dev/null || true
```

4. **Edit transcript** (important for F5):

```bash
nano data/reference_transcript.txt
# Write EXACTLY what you said in reference.wav (Malay OK)
```

Or auto ASR (uses extra GPU memory):

```bash
--auto-transcribe
```

5. **Generate F5 samples**:

```bash
source /workspace/modeOn/.venv-f5/bin/activate
cd /workspace/modeOn
python3 scripts/week1_validate_f5.py \
  --ref-audio /workspace/voices/default/reference.wav \
  --limit 10 \
  --output-dir /workspace/samples/week1-f5
```

6. **Download & listen** — same 10 sentences, two folders:
   - `week1/01.wav` (XTTS)
   - `week1-f5/01.wav` (F5)

7. **Stop pod** when finished.

---

## Score sheet (fill after listening)

| # | XTTS clarity | F5 clarity | XTTS natural | F5 natural | Notes |
|---|--------------|------------|--------------|------------|-------|
| 1 | | | | | |
| … | | | | | |

**Decision:**

- F5 clearly better → fine-tune / productize on **F5** (or hybrid)
- Both weak → more data + fine-tune, or try Fish Speech
- XTTS better → stay Coqui path

---

## License note

F5-TTS and Coqui models have their own licenses (check repos before commercial use).
