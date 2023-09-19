from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Kafka comsumer worker"
    test_mode: bool = True
    KAFKA_INSTANCE: str = ''

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()