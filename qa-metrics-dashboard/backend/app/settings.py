from pydantic import BaseModel
import os

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    allowed_origins: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    admin_email: str = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "Admin@12345")
    viewer_email: str = os.getenv("VIEWER_EMAIL", "viewer@example.com")
    viewer_password: str = os.getenv("VIEWER_PASSWORD", "Viewer@12345")

settings = Settings()
