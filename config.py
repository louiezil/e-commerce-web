import os


class Config:
    DATABASE = os.environ.get("DATABASE", "database.db")
    DEBUG = os.environ.get("DEBUG", "true").lower() == "true"
    SECRET_KEY = os.environ.get("SECRET_KEY", "the-secret-key")

    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = 86400