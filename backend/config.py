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
class ProductionConfig(BaseConfig):
    debug = False

