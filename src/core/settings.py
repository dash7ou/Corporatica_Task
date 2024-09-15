from pydantic_settings import SettingsConfigDict, BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.parent / ".env")




settings = Settings() # type: ignore # will be propagated by .env file at runtime
