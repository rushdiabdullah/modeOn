from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import tts
from tts.config import get_settings
from tts.engine import TTSEngine, build_engine

_tts_engine: TTSEngine | None = None


def get_tts_engine() -> TTSEngine:
    if _tts_engine is None:
        raise RuntimeError("TTS engine not initialized")
    return _tts_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _tts_engine
    settings = get_settings()
    _tts_engine = build_engine(settings)
    yield
    _tts_engine = None


app = FastAPI(
    title="modeOn Voice API",
    description="Malaysian neural TTS API (XTTS v2)",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(tts.router)


@app.get("/health")
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "tts_mode": settings.modeon_tts_mode,
        "engine_loaded": _tts_engine is not None,
    }
