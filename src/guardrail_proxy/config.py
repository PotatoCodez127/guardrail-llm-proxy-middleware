# src/guardrail_proxy/config.py
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProxySettings(BaseSettings):
    ollama_api_base_url: HttpUrl = "https://ollama.com"
    ollama_api_key: str
    primary_model: str = "gemma4:31b-cloud"
    judge_model: str = "gemma4:31b-cloud"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
