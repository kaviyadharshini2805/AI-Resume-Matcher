from pydantic import BaseModel
import os

class Settings(BaseModel):
    PROJECT_NAME: str = "AI Resume Matcher API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    DATABASE_URL: str = "sqlite:///./resume_matcher.db"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
