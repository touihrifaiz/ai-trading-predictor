from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_vision_model: str = "gpt-4.1-mini"
    twelve_data_api_key: str = ""
    cors_origins: list[str] = ["http://localhost:5173", "capacitor://localhost", "http://localhost"]
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
