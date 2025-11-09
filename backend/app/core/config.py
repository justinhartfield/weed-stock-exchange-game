from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/strainexchange"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-this"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Metabase
    METABASE_URL: str = ""
    METABASE_USERNAME: str = ""
    METABASE_PASSWORD: str = ""
    
    # Game Settings
    INITIAL_WEEDCOINS: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
