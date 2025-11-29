from flask import Flask
from models import *
from config import LocalDevelopmentConfig
from flask_cors import CORS

from flask_security import Security, SQLAlchemyUserDatastore
from database import cache, mail


from database import security 

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)

db.init_app(app)
cache.init_app(app) 
mail.init_app(app)  

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, datastore)
app.datastore = datastore


from resources import auth_bp, api_bp 

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)