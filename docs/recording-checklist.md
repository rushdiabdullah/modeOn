# Reference voice recording checklist

**Goal:** 2–4 hours clean speech (Phase 1 quality). Minimum for zero-shot demo: 6–30 seconds.

## Environment

- [ ] Quiet room, no echo (clothes closet or carpeted room works)
- [ ] Same mic and distance for whole session
- [ ] No fan/AC blowing toward mic

## Format

- [ ] WAV or FLAC, mono preferred
- [ ] 24 kHz or 48 kHz sample rate
- [ ] Peak around -12 dB to -6 dB (no clipping)

## Content

- [ ] Varied BM sentences (see `tests/sentences_ms.txt`)
- [ ] Numbers, names, loanwords, short and long lines
- [ ] Consistent persona (pace, energy)
- [ ] Pause 1 s between takes; trim long silences later

## Legal

- [ ] Written consent from voice owner (PDPA)
- [ ] Clear whether voice is for internal demo or commercial clone

## After recording

- [ ] Store under `data/recordings/` (gitignored)
- [ ] Export one **reference clip** (6–30 s) to RunPod volume for XTTS
- [ ] Backup raw files outside the pod
