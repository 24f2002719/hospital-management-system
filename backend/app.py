from flask import Flask
from models import *
from config import LocalDevelopmentConfig
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from resources import auth_bp, api,api_bp
from flask_cors import CORS




def create_app():
    app = Flask(__name__)

    

    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    # For Flask Sequrity
    from flask_security.datastore import SQLAlchemyUserDatastore
    from database import security

    datastore = SQLAlchemyUserDatastore(db,User,Role)
    security.init_app(app, datastore)

    app.datastore = datastore

    # Blueprint
    app.register_blueprint(auth_bp)

    #Flask Restful API
    app.register_blueprint(api_bp)


    with app.app_context():
        db.create_all()
    return app

app = create_app()

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
