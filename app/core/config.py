from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Customer Support Resolution Agent"
    app_env: str = "development"
    debug: bool = True
    
    database_url: str
    checkpoint_database_url: str

    raw_data_path: str = "data/raw/customer_support_tickets.csv"
    processed_data_path: str = (
        "data/processed/customer_support_tickets_clean.csv"
    )

    mistral_api_key: str
    mistral_model: str = "mistral-small-latest"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 500

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()