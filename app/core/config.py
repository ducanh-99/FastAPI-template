import json
import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):

    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Lead management api')
    DEBUG: bool = os.getenv('DEBUG', 'False')
    SECRET_KEY: Optional[str] = os.getenv('SECRET_KEY', '')
    ALGORITHM: Optional[str] = os.getenv('ALGORITHM', '')
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[str] = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    BACKEND_CORS_ORIGINS: Optional[list] = ["*"]
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * \
        60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM: Optional[str] = 'HS256'
    LOGGING_CONFIG_FILE: Optional[str] = os.path.join(BASE_DIR, 'logging.ini')

    # db
    DATABASE_URL: Optional[str] = os.getenv(
        'SQL_DATABASE_URL', 'sqlite:///.db')

    # s3
    MINIO_ENDPOINT: Optional[str] = os.getenv('MINIO_ENDPOINT', '')
    MINIO_ACCESS_KEY: Optional[str] = os.getenv('MINIO_ACCESS_KEY', '')
    MINIO_SECRET_KEY: Optional[str] = os.getenv('MINIO_SECRET_KEY', '')
    BUCKET_NAME: Optional[str] = os.getenv('BUCKET_NAME', '')

    # Storage local
    FS_DIRECTORY: Optional[str] = os.getenv("FS_DIRECTORY", "/tmp")

    # RAM
    KAFKA_CONN_STR: str = os.getenv('KAFKA_CONN_STR')


settings = Settings()
