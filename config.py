import os


class Config:
    # Flask configuratie
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = "sqlite:///survey.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin credentials
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

    # Server configuratie
    PORT = int(os.environ.get("PORT", 8000))
    DEBUG = False
