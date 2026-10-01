from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_key: str = "dev-insecure-change-me"
    modeon_tts_mode: Literal["mock", "xtts"] = "mock"

    model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    device: str = "cuda"
    model_path: str = ""
    default_speaker_wav: str = ""

    max_text_chars: int = 500


@lru_cache
def get_settings() -> Settings:
    return Settings()
