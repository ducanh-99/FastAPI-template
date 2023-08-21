import json
import os

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'Lead management api')
    DEBUG: bool = os.getenv('DEBUG', 'False')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    ALGORITHM = os.getenv('ALGORITHM', '')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    BACKEND_CORS_ORIGINS = ['*']
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')

    APP_ID = "LM"

    DOMAIN = os.getenv("DOMAIN")

    # db
    DATABASE_URL = os.getenv('SQL_DATABASE_URL', 'sqlite:///.db')

    # s3
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', '')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', '')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', '')
    BUCKET_NAME = os.getenv('BUCKET_NAME', '')

    # Storage local
    FS_DIRECTORY = os.getenv("FS_DIRECTORY", "/tmp")

    # RAM
    KAFKA_CONN_STR: str = os.getenv('KAFKA_CONN_STR')

    GOOGLE_CREDENTIALS = json.loads(os.getenv('GOOGLE_CREDENTIAL'))

    # TWILIO
    ACCOUNT_SID_TWILIO: str = os.getenv("ACCOUNT_SID_TWILIO")
    AUTH_TOKEN_TWILIO: str = os.getenv("AUTH_TOKEN_TWILIO")

    BOOKING_CREATE_TOPIC: str = os.getenv('BOOKING_CREATE_TOPIC', 'booking')
    EVENT_UPDATE_STATUS_TOPIC: str = os.getenv('EVENT_UPDATE_STATUS_TOPIC', 'event-update-status')
    PAYMENT_TOPIC: str = os.getenv('PAYMENT_TOPIC', 'payment')

    CONSUME_EVENT_UPDATE_STATUS: str = os.getenv("CONSUME_EVENT_UPDATE_STATUS", 'event-update-status-consumer')
    CONSUME_BOOKING_CREATE: str = os.getenv("CONSUME_BOOKING_CREATE", 'booking-create-consume-group')
    CONSUME_PAYMENT: str = os.getenv("CONSUME_PAYMENT", 'payment-consume')


settings = Settings()
