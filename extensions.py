import logging
import os
from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config
from urllib.parse import urlparse

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

logging.debug("Initializing extensions.py")

# Initialize PyMongo with error handling
mongo = None
try:
    mongo_uri = app.config.get('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in the application config")
    
    parsed_uri = urlparse(mongo_uri)
    logging.debug(f"Attempting to connect to MongoDB:")
    logging.debug(f"  Scheme: {parsed_uri.scheme}")
    logging.debug(f"  Hostname: {parsed_uri.hostname}")
    logging.debug(f"  Port: {parsed_uri.port}")
    logging.debug(f"  Username: {'*' * len(parsed_uri.username) if parsed_uri.username else 'None'}")
    logging.debug(f"  Password: {'*' * 8 if parsed_uri.password else 'None'}")
    logging.debug(f"  Database: {parsed_uri.path[1:] if parsed_uri.path else 'None'}")
    
    mongo = PyMongo(app)
    
    # Test the connection
    mongo.db.command('ping')
    logging.info("MongoDB connection established successfully")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {str(e)}")
    logging.exception("Detailed MongoDB connection error:")

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    try:
        from models import User
        return User.get_user_by_id(user_id)
    except Exception as e:
        logging.error(f"Error loading user: {str(e)}")
        logging.exception("Detailed user loading error:")
        return None

logging.debug("Finished initializing extensions.py")
