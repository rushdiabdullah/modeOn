from __future__ import annotations

import io
import struct
import wave
from abc import ABC, abstractmethod
from pathlib import Path

from tts.config import Settings


class TTSEngine(ABC):
    @abstractmethod
    def synthesize(
        self,
        text: str,
        *,
        speaker_id: str,
        language: str,
        speed: float,
    ) -> bytes:
        raise NotImplementedError


def _mock_wav_bytes(duration_sec: float = 0.4, sample_rate: int = 24000) -> bytes:
    n_frames = int(sample_rate * duration_sec)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frame = struct.pack("<h", 0)
        wf.writeframes(frame * n_frames)
    return buf.getvalue()


class MockEngine(TTSEngine):
    def synthesize(
        self,
        text: str,
        *,
        speaker_id: str,
        language: str,
        speed: float,
    ) -> bytes:
        duration = min(2.0, 0.15 + len(text) * 0.008) / max(speed, 0.5)
        return _mock_wav_bytes(duration_sec=duration)


class XTTSEngine(TTSEngine):
    def __init__(self, settings: Settings) -> None:
        try:
            from TTS.api import TTS
        except ImportError as e:
            raise RuntimeError(
                "Coqui TTS not installed. On RunPod: pip install TTS==0.22.0 torch torchaudio"
            ) from e

        self._settings = settings
        model_id = settings.model_path.strip() or settings.model_name
        self._tts = TTS(model_id).to(settings.device)
        self._speaker_wav = settings.default_speaker_wav

    def _resolve_speaker_wav(self, speaker_id: str) -> str:
        if speaker_id == "default":
            path = self._speaker_wav
        else:
            path = str(Path("/runpod-volume/voices") / speaker_id / "reference.wav")
        if not path or not Path(path).is_file():
            raise ValueError(
                f"No reference WAV for speaker_id={speaker_id!r}. "
                "Set DEFAULT_SPEAKER_WAV or add /runpod-volume/voices/<id>/reference.wav"
            )
        return path

    def synthesize(
        self,
        text: str,
        *,
        speaker_id: str,
        language: str,
        speed: float,
    ) -> bytes:
        import os
        import tempfile

        speaker_wav = self._resolve_speaker_wav(speaker_id)
        fd, out_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        out = Path(out_path)
        try:
            self._tts.tts_to_file(
                text=text,
                file_path=str(out),
                speaker_wav=speaker_wav,
                language=language,
                speed=speed,
            )
            return out.read_bytes()
        finally:
            out.unlink(missing_ok=True)


def build_engine(settings: Settings) -> TTSEngine:
    if settings.modeon_tts_mode == "mock":
        return MockEngine()
    return XTTSEngine(settings)
