from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SMS Blast API"
    test_mode: bool = True
    test_phone_nums: list = []
    wg_url: str = 'https://frog.wigal.com.gh/api/v2/sendmsg'
    wg_username: str
    wg_password: str
    wg_senderid: str
    KAFKA_INSTANCE: str = ''

    model_config = SettingsConfigDict(env_file=".env_cons")
    # model_config = SettingsConfigDict(env_file=".env")

settings = Settings()