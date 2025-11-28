from flask import Flask
from models import *
from config import LocalDevelopmentConfig
from flask_cors import CORS

from flask_security import Security, SQLAlchemyUserDatastore
from database import cache, mail


# Note: Ensure you have 'security' object defined in 'database.py' or import Security class directly
from database import security 

# --- 1. INITIALIZE APP & EXTENSIONS GLOBALLY ---
app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)

# Initialize DB
db.init_app(app)
cache.init_app(app) # <--- Init Cache
mail.init_app(app)  # <--- Init Mail

# Initialize CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# # Initialize Mail (CRITICAL: Must be done here so tasks.py can import it)
# mail = Mail(app)

# # 2. Initialize Cache
# cache = Cache(app)

# Initialize Security
datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, datastore)
app.datastore = datastore

# --- 2. IMPORT & REGISTER BLUEPRINTS (DO THIS LAST) ---
# We import resources here to avoid "Circular Import" errors.
# If we import at the top, resources will try to load tasks, 
# which try to load 'mail' from app, which wouldn't exist yet!
from resources import auth_bp, api_bp 

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

# --- 3. CREATE DATABASE TABLES ---
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)