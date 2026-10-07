from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SMMS™ - Service Model Management System"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    POSTGRES_URL: str | None = None
    SQLITE_URL: str = "sqlite+aiosqlite:///./smms.db"

    @computed_field
    def DATABASE_URL(self) -> str:
        if self.POSTGRES_URL:
            # Ensure it uses the asyncpg driver
            if self.POSTGRES_URL.startswith("postgresql://"):
                return self.POSTGRES_URL.replace(
                    "postgresql://", "postgresql+asyncpg://", 1
                )
            return self.POSTGRES_URL
        return self.SQLITE_URL

    # LLM settings
    LLM_PROVIDER: str = "groq"  # options: "local", "groq"
    GROQ_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )


settings = Settings()
