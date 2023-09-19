# from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MegaFortune API (writer updates)"
    TEST_MODE: bool = False

    HASURA_GRAPHQL_URL:str = ""
    HASURA_GRAPHQL_SECRET:str = ""
    HASURA_GRAPHQL_TOKEN:str = ""

    APP_BASE_URL: str = ''
    WIGAL_SMS_URL: str = ''
    WIGAL_SMS_USERNAME: str = ''
    WIGAL_SMS_PASSWORD: str = ''
    DEFAULT_SMS_PROVIDER: str = 'wigal'
    
    HUBTEL_CHECK_PAYOUT_STATUS: str = ''
    HUBTEL_MERCHANT_ACCOUNT_NO: str = ''
    HUBTEL_PAYMENT_AUTH_TOKEN: str = ''
    HUBTEL_PAYMENT_URL: str = ''
    HUBTEL_MOMO_TRANSFER_URL_STAGING:str = ''

    AUTH_ALGORITHMS: str = ''
    AUTH_SECRET: str = ''
    AUTH_WEB_TOKEN_EXPIRY_SECONDS: str = ''
    AUTH_MOBILE_TOKEN_EXPIRY_SECONDS: str = ''
    AUTH_OTP_EXPIRY_SECONDS: str = ''

    SENDGRID_URL: str = ''
    SENDGRID_API_KEY: str = ''
    FROM_EMAIL: str = ''
    FROM_NAME: str = 'MegaFortune'
    PORT= "8000"
    SMS_URL: str = ''
    SMS_KEY: str = ''
    SMS_SECRET: str = ''
    SMS_SENDER_ID: str = 'MegaFortune'
    HUBTEL_MOMO_TRANSFER_URL: str = ''
    HUBTEL_PAYMENT_RETURN_URL: str = ''
    S3_ACCESS_ID: str = ''
    S3_SECRET_ACCESS_KEY: str = ''
    S3_DEFAULT_BUCKET: str = ''
    FCM_KEY: str = ''
    KAFKA_INSTANCE: str = 'kafka1:9092'
    HUBTEL_CHECK_TRANSACTION_STATUS: str = ''

    # model_config = SettingsConfigDict(env_file=".env")
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()