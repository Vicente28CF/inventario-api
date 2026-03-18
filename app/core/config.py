from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    resend_api_key: str = ""
    alert_email: str = ""
    TESTING: bool = False

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()