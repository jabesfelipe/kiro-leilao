"""Configuração da aplicação (12-factor, desacoplada por env)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RADAR_", env_file=".env", extra="ignore")

    # LLM desacoplado por configuração (arquitetura §3: OpenAI como primeiro provedor)
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str = ""

    # Banco (arquitetura §3: PostgreSQL + pgvector)
    database_url: str = "postgresql+psycopg://radar:radar@localhost:5432/radar"
    db_schema: str = "poc_ia"
    # Override de IP para RDS em VPC privada (hostname não resolve fora da VPC).
    db_host_addr: str | None = None

    # Local-first no MVP
    environment: str = "local"

    def sqlalchemy_url(self) -> str:
        """URL final; injeta hostaddr+sslmode quando db_host_addr está definido."""
        url = self.database_url
        if self.db_host_addr:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}hostaddr={self.db_host_addr}&sslmode=require"
        return url


settings = Settings()
