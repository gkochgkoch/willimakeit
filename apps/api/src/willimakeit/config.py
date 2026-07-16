from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

API_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    rapidapi_key: str = ""
    aerodatabox_base_url: str = "https://aerodatabox.p.rapidapi.com"
    aerodatabox_timeout_seconds: float = 10.0

    model_config = SettingsConfigDict(
        env_file=API_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
