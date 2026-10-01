#!/usr/bin/env python3
"""Week 1 compare: F5-TTS samples + latency (RunPod GPU)."""

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


def load_ref_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8").strip()
    lines = [ln for ln in raw.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    return " ".join(lines).strip()


def word_count(text: str) -> int:
    return len(text.split())


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week 1 F5-TTS validation samples")
    parser.add_argument("--ref-audio", required=True, help="Reference WAV path")
    parser.add_argument(
        "--ref-text",
        default="",
        help="Exact transcript of reference audio (required unless --auto-transcribe)",
    )
    parser.add_argument(
        "--ref-text-file",
        type=Path,
        default=Path("data/reference_transcript.txt"),
        help="File with reference transcript (used if --ref-text empty)",
    )
    parser.add_argument(
        "--auto-transcribe",
        action="store_true",
        help="Let F5 ASR transcribe ref audio (uses extra VRAM)",
    )
    parser.add_argument("--sentences", type=Path, default=Path("tests/sentences_ms.txt"))
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output-dir", type=Path, default=Path("samples/week1-f5"))
    parser.add_argument("--nfe-step", type=int, default=32, help="F5 diffusion steps (quality vs speed)")
    args = parser.parse_args()

    ref_audio = Path(args.ref_audio)
    if not ref_audio.is_file():
        print(f"ERROR: ref audio not found: {ref_audio}", file=sys.stderr)
        return 1

    ref_text = args.ref_text.strip()
    if not ref_text and not args.auto_transcribe:
        if args.ref_text_file.is_file():
            ref_text = load_ref_text(args.ref_text_file)
        if not ref_text or ref_text.startswith("Isi transkrip"):
            print(
                "ERROR: Set --ref-text or edit data/reference_transcript.txt "
                "(exact words in reference.wav), or use --auto-transcribe",
                file=sys.stderr,
            )
            return 1

    if args.auto_transcribe:
        ref_text = ""

    try:
        from f5_tts.api import F5TTS
    except ImportError:
        print("ERROR: pip install -r requirements-f5.txt (use .venv-f5)", file=sys.stderr)
        return 1

    sentences = load_sentences(args.sentences, args.limit)
    if not sentences:
        print("ERROR: no sentences", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("==> loading F5-TTS (first run downloads weights) ...")
    t0 = time.perf_counter()
    tts = F5TTS()
    load_s = time.perf_counter() - t0
    print(f"==> model ready in {load_s:.1f}s")

    rows: list[dict] = []
    for idx, text in enumerate(sentences, start=1):
        out = args.output_dir / f"{idx:02d}.wav"
        start = time.perf_counter()
        tts.infer(
            ref_file=str(ref_audio),
            ref_text=ref_text,
            gen_text=text,
            nfe_step=args.nfe_step,
            file_wave=str(out),
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
    manifest = {
        "engine": "f5-tts",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ref_audio": str(ref_audio),
        "ref_text_source": "auto" if args.auto_transcribe else "provided",
        "nfe_step": args.nfe_step,
        "model_load_s": round(load_s, 2),
        "samples": rows,
        "summary": {
            "count": len(rows),
            "latency_mean_s": round(statistics.mean(latencies), 3),
            "latency_p95_s": round(sorted(latencies)[max(0, int(0.95 * len(latencies)) - 1)], 3),
        },
    }
    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n==> done. manifest: {manifest_path}")
    print("Compare with XTTS: samples/week1/ vs samples/week1-f5/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
