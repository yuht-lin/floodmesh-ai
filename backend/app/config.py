from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./floodmesh.db"
    
    # Gemini API Settings
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.7-flash"
    
    # CORS Configuration
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173"

    @property
    def parsed_cors_origins(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return self.CORS_ORIGINS

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
