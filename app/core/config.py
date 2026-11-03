from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INSECURE_ADMIN_API_KEYS = {
    "",
    "change-me-in-production",
    "replace_with_a_long_random_secret",
}


class Settings(BaseSettings):
    app_name: str = "Enterprise HR Policy Agentic RAG Copilot"
    app_env: str = "development"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    llm_provider: str = "gemini"
    tavily_api_key: str = ""
    pinecone_api_key: str = ""
    pinecone_index_name: str = "fde-hr-policy-rag"
    pinecone_namespace: str = "company-hr-kb"
    embedding_model: str = "text-embedding-004"
    gemini_model: str = "gemini-3.8-flash"
    openai_model: str = "gpt-4o-mini"
    top_k: int = 4
    max_retries: int = 1
    admin_api_key: str = "change-me-in-production"
    audit_db_path: str = str(BASE_DIR / "data" / "audit.db")
    upload_dir: str = str(BASE_DIR / "uploads")
    sample_kb_dir: str = str(BASE_DIR / "data" / "sample_kb")
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")

    @model_validator(mode="after")
    def require_secure_production_admin_key(self) -> "Settings":
        if self.app_env.strip().casefold() == "production":
            admin_key = self.admin_api_key.strip()
            if admin_key.casefold() in INSECURE_ADMIN_API_KEYS:
                raise ValueError(
                    "Production requires a non-empty ADMIN_API_KEY that is not a placeholder."
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()