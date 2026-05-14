from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"
    platform_api_keys: str = ""
    platform_api_key_hashes: str = ""
    max_request_bytes: int = 2_000_000

    enforce_tenant_jwt: bool = False
    tenant_jwt_secret: str = ""
    tenant_jwt_issuer: str = "mattjames-auth"
    tenant_jwt_audience: str = "mattjames-platform"

    database_url: str = "postgresql://postgres:postgres@localhost:5432/mj_platform"
    use_inmemory_store: bool = False

    @property
    def api_keys(self) -> set[str]:
        return {item.strip() for item in self.platform_api_keys.split(",") if item.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
