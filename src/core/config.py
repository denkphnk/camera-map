from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    JWT_SECRET_KEY: str
    ENVIRONMENT: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()