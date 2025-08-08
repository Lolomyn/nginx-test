from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    project_name: str = Field(default="AuthService", alias="PROJECT_NAME")
    environment: str = Field(default="dev", alias="ENVIRONMENT")

    database_url: str = Field(alias="DATABASE_URL")

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = Field(alias="JWT_REFRESH_SECRET_KEY")
    access_token_expire_minutes: int = Field(default=15, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(default=60 * 24 * 7, alias="REFRESH_TOKEN_EXPIRE_MINUTES")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")


settings = Settings()