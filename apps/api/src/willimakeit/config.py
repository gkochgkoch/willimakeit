from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

API_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    rapidapi_key: str = ""
    aerodatabox_base_url: str = "https://aerodatabox.p.rapidapi.com"
    timeout: float = 10.0
    openmeteo_base_url: str = "https://api.open-meteo.com/v1/forecast"
    ollama_base_url: str = "http://localhost:11434/v1/"
    ollama_model: str = "qwen3:4b"
    ollama_host: str = "localhost:11434"
    embedding_model: str = "qwen3-embedding:0.6b"
    redis_url: str = "redis://localhost:6379"
    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=API_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
