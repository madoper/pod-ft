__anchor__ = "telegram-settings"
# schema-ref: project-schema.yaml#/shared_modules/1

from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    bot_token: str = ""
    api_base_url: str = "http://gateway:8000/api/v1"
    api_key: str = ""
    max_question_length: int = 1000
    poll_interval_sec: float = 2.0
    poll_max_attempts: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


bot_settings = BotSettings()
