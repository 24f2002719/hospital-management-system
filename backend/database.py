from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_caching import Cache # Import Cache
from flask_mail import Mail     # Import Mail

security = Security()
db = SQLAlchemy()
cache = Cache()  # <--- Define Cache Here
mail = Mail()    # <--- Define Mail Here