"""
config/settings.py
Application configuration settings
"""

import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration shared across all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16 MB
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "data/uploads")
    ALLOWED_EXTENSIONS = {"csv", "txt", "json"}


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    DEBUG = True
    TESTING = True


# Map environment name to config class
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)
