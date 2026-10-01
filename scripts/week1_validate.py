#!/usr/bin/env python3
"""Week 1: batch XTTS samples + latency report (run on RunPod GPU)."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def load_sentences(path: Path, limit: int) -> list[str]:
    lines = [
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    return lines[:limit]


def word_count(text: str) -> int:
    return len(text.split())


def xtts_language(code: str) -> str:
    """XTTS v2 has no `ms`; BM sentences use `en` + Malay reference voice."""
    normalized = code.strip().lower()
    if normalized in ("ms", "bm", "ms-my", "malay"):
        return "en"
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week 1 XTTS validation samples")
    parser.add_argument(
        "--speaker-wav",
        required=True,
        help="Reference clip for zero-shot cloning (6–30 s clean WAV)",
    )
    parser.add_argument("--sentences", type=Path, default=Path("tests/sentences_ms.txt"))
    parser.add_argument("--limit", type=int, default=10, help="Number of sentences (default 10)")
    parser.add_argument("--output-dir", type=Path, default=Path("samples/week1"))
    parser.add_argument(
        "--language",
        default="en",
        help="XTTS language code (use en for BM text; ms is mapped to en automatically)",
    )
    parser.add_argument("--device", default="cuda")
    parser.add_argument(
        "--model",
        default="tts_models/multilingual/multi-dataset/xtts_v2",
    )
    args = parser.parse_args()

    speaker = Path(args.speaker_wav)
    if not speaker.is_file():
        print(f"ERROR: speaker wav not found: {speaker}", file=sys.stderr)
        return 1
    if not args.sentences.is_file():
        print(f"ERROR: sentences file not found: {args.sentences}", file=sys.stderr)
        return 1

    try:
        from TTS.api import TTS
    except ImportError:
        print(
            "ERROR: Coqui TTS not installed. Run: pip install -r requirements-gpu.txt",
            file=sys.stderr,
        )
        return 1

    sentences = load_sentences(args.sentences, args.limit)
    if not sentences:
        print("ERROR: no sentences loaded", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    lang = xtts_language(args.language)
    if lang != args.language.strip().lower():
        print(f"==> language {args.language!r} -> XTTS uses {lang!r} (BM text + reference voice)")

    print(f"==> loading model {args.model} on {args.device} ...")
    t0 = time.perf_counter()
    tts = TTS(args.model).to(args.device)
    load_s = time.perf_counter() - t0
    print(f"==> model loaded in {load_s:.1f}s")

    warmup = "Ujian pemanasan model."
    warm_path = args.output_dir / "_warmup.wav"
    print("==> warmup synthesis ...")
    tts.tts_to_file(
        text=warmup,
        file_path=str(warm_path),
        speaker_wav=str(speaker),
        language=lang,
    )

    rows: list[dict] = []
    for idx, text in enumerate(sentences, start=1):
        out = args.output_dir / f"{idx:02d}.wav"
        start = time.perf_counter()
        tts.tts_to_file(
            text=text,
            file_path=str(out),
            speaker_wav=str(speaker),
            language=lang,
        )
        elapsed = time.perf_counter() - start
        wc = word_count(text)
        rows.append(
            {
                "index": idx,
                "file": str(out),
                "text": text,
                "word_count": wc,
                "latency_s": round(elapsed, 3),
            }
        )
        print(f"  [{idx:02d}] {elapsed:.2f}s ({wc} words) -> {out.name}")

    latencies = [r["latency_s"] for r in rows]
    near_30 = [r for r in rows if 25 <= r["word_count"] <= 35]
    if not near_30:
        near_30 = sorted(rows, key=lambda r: abs(r["word_count"] - 30))[:1]

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "device": args.device,
        "language": lang,
        "language_requested": args.language,
        "speaker_wav": str(speaker),
        "model_load_s": round(load_s, 2),
        "samples": rows,
        "summary": {
            "count": len(rows),
            "latency_mean_s": round(statistics.mean(latencies), 3),
            "latency_p95_s": round(sorted(latencies)[max(0, int(0.95 * len(latencies)) - 1)], 3),
            "latency_30w_ref_s": near_30[0]["latency_s"] if near_30 else None,
            "latency_30w_ref_text": near_30[0]["text"][:80] if near_30 else None,
        },
    }

    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print("")
    print("==> summary")
    print(f"  mean latency: {manifest['summary']['latency_mean_s']}s")
    print(f"  p95 latency:  {manifest['summary']['latency_p95_s']}s")
    if manifest["summary"]["latency_30w_ref_s"] is not None:
        print(f"  ~30-word ref: {manifest['summary']['latency_30w_ref_s']}s")
    print(f"  manifest:     {manifest_path}")
    print("")
    print("Next: listen to samples/week1/*.wav and fill docs/validation-week1.md")

    scoring_path = args.output_dir / "scoring-template.md"
    if not scoring_path.exists():
        lines = [
            "# Week 1 listening scores (fill after you listen)",
            "",
            "| # | File | Clarity 1–5 | BM 1–5 | Natural 1–5 | Notes |",
            "|---|------|-------------|--------|-------------|-------|",
        ]
        for r in rows:
            excerpt = r["text"][:40] + ("…" if len(r["text"]) > 40 else "")
            lines.append(f"| {r['index']} | `{Path(r['file']).name}` | | | | {excerpt} |")
        lines.extend(
            [
                "",
                "**Go/no-go:** clarity avg ≥ 3.5 and you'd show one sample to a trusted listener.",
                "",
            ]
        )
        scoring_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  scoring template: {scoring_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
