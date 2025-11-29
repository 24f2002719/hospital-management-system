from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_caching import Cache 
from flask_mail import Mail    

security = Security()
db = SQLAlchemy()
cache = Cache()  
mail = Mail()    