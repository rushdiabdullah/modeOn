#!/usr/bin/env python3
"""Simple latency check against a running modeOn API."""

from __future__ import annotations

import argparse
import os
import statistics
import time
import urllib.error
import urllib.request


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark POST /v1/tts")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key", default=os.environ.get("API_KEY", ""))
    parser.add_argument("--text", default="Ini ujian latency tiga puluh patah perkataan lebih kurang.")
    parser.add_argument("-n", type=int, default=5)
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Set API_KEY env or pass --api-key")

    url = f"{args.base_url.rstrip('/')}/v1/tts"
    body = (
        '{"text":'
        + __import__("json").dumps(args.text)
        + ',"speaker_id":"default","language":"ms","speed":1.0}'
    ).encode()

    times: list[float] = []
    for _ in range(args.n):
        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": args.api_key,
            },
        )
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                resp.read()
        except urllib.error.HTTPError as e:
            raise SystemExit(f"HTTP {e.code}: {e.read().decode()}") from e
        times.append(time.perf_counter() - start)

    print(f"runs={args.n}")
    print(f"mean_s={statistics.mean(times):.3f}")
    if len(times) > 1:
        print(f"p95_s={sorted(times)[int(0.95 * len(times)) - 1]:.3f}")


if __name__ == "__main__":
    main()
