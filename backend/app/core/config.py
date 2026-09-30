from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PharmaStock AI"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "sqlite:///./pharmastock.db"

    jwt_secret: str = "change-me-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    cookie_name: str = "access_token"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    cookie_domain: str = ""
    cookie_path: str = "/"

    cors_origins: str = "http://localhost:5173"

    ocr_upload_dir: str = "uploads/invoices"
    tesseract_cmd: str = ""

    whatsapp_api_url: str = "https://graph.facebook.com/v19.0"
    whatsapp_api_token: str = ""
    whatsapp_phone_number_id: str = ""

    drug_license_api_url: str = ""
    drug_license_api_key: str = ""

    seed_admin_email: str = "admin@pharmastock.example"
    seed_admin_password: str = "ChangeMeAdmin123!"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def cookie_samesite_normalized(self) -> str:
        value = (self.cookie_samesite or "lax").lower()
        if value not in {"lax", "strict", "none"}:
            return "lax"
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
