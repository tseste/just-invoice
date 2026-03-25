"""Application configuration."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Default application settings from environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    PDF_OUTPUT_DIR = os.environ.get("PDF_OUTPUT_DIR", "assets/invoices")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_USER = os.environ.get("DB_USER", "")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_NAME = os.environ.get("DB_NAME", "")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    BABEL_DEFAULT_LOCALE = os.environ.get("BABEL_DEFAULT_LOCALE", "el")
    BABEL_TRANSLATION_DIRECTORIES = os.environ.get(
        "BABEL_TRANSLATION_DIRECTORIES", str(BASE_DIR / "translations")
    )
