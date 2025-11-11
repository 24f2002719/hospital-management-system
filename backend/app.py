from flask import Flask
from models import *
from config import LocalDevelopmentConfig
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt




def create_app():
    app = Flask(__name__)

    

    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    # For Flask Sequrity
    from flask_security.datastore import SQLAlchemyUserDatastore
    from database import security

    datastore = SQLAlchemyUserDatastore(db,User,Role)
    security.init_app(app, datastore)

    app.datastore = datastore


    with app.app_context():
        db.create_all()
    return app

app = create_app()

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
