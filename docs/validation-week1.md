# Week 1 validation

**Date:** 2026-10-01  
**Pod:** modeon-week1 (RTX 3090, Community)  
**Reference:** ~10 s WAV from `download/referrence.m4a`  
**Stack:** TTS 0.22.0, torch 2.5.1, transformers 4.33.3, language `en` for BM text  

**Latency (manifest on pod):** mean ~4.2 s, p95 ~6.9 s  

## Listening result

| # | Clarity 1–5 | BM 1–5 | Natural 1–5 | Notes |
|---|-------------|--------|-------------|-------|
| 1–10 | ~2–3 | ~2 | ~2 | English slang prosody, robotic; zero-shot + `en` lang |

**Averages (subjective):** Clarity ~2.5 | BM ~2 | Natural ~2  

**Go/no-go:** **NO-GO** for product voice — **GO** for pipeline (model runs, 10 WAVs generated).  

**Next action:** Fine-tune / more reference data / engine compare before Week 2 client demo.  
