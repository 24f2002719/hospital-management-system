import os
from dotenv import load_dotenv


load_dotenv()
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATION = False

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

