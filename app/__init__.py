from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_login import LoginManager
import os

load_dotenv()

# Initialize Flask-Login
login_manager = LoginManager()

# Initialize MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

def create_app():
    app = Flask(__name__)
    
    # Configure Flask-Login
    login_manager.init_app(app)
    
    # Set secret key
    app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # Import and register blueprints here
    from .routes.home import home_bp
    from .routes.auth import auth_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    
    return app