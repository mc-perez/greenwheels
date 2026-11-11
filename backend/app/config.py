from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_DATABASE_URL = (
    "postgresql+psycopg://greenwheels:greenwheels@localhost:5433/greenwheels"
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = _DEFAULT_DATABASE_URL

    @field_validator("database_url", mode="before")
    @classmethod
    def reject_blank_database_url(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return _DEFAULT_DATABASE_URL
        return value


settings = Settings()
