from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    platform_api_url: str = "http://localhost:3000"
    model_provider: str = "fake"
    inference_region: str = "ap-south-1"
    default_tenant_daily_budget_cents: int = 500


settings = Settings()
