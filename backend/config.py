import os
from dotenv import load_dotenv


load_dotenv()
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATION = False

    # --- CELERY CONFIG ---
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    CELERY_TIMEZONE = "Asia/Kolkata" # Change to your timezone

    # --- FLASK MAIL (MailHog) ---
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'noreply@hospital.com'

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://127.0.0.1:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300  # Default cache life: 5 minutes
    CACHE_KEY_PREFIX = "hms_"    # Prefix for keys in Redis

class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    debug = True
    SECRET_KEY= os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT= os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = 'argon2'

    WTF_CSRF_ENABLED = False   # Disable CSRF for API
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token' # Tell Flask which header to look for
    SECURITY_TRACKABLE = True
    WTF_CSRF_CHECK_DEFAULT = False


class ProductionConfig(BaseConfig):
    debug = False

