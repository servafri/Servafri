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
    # Use local MongoDB instance by default
    app.config['MONGO_URI'] = "mongodb://localhost:27017/servafri_cloud"
    mongo = PyMongo(app)
    mongo.db.command('ping')
    logging.info("Connected to local MongoDB instance successfully")
except Exception as local_e:
    logging.error(f"Error connecting to local MongoDB: {str(local_e)}")
    logging.exception("Detailed local MongoDB connection error:")
    
    # Fallback to MongoDB Atlas if local connection fails
    try:
        mongo_uri = os.environ.get('MONGO_URI')
        if mongo_uri:
            app.config['MONGO_URI'] = mongo_uri
            mongo = PyMongo(app)
            mongo.db.command('ping')
            logging.info("Connected to MongoDB Atlas successfully")
        else:
            raise ValueError("MONGO_URI environment variable is not set")
    except Exception as atlas_e:
        logging.error(f"Error connecting to MongoDB Atlas: {str(atlas_e)}")
        logging.exception("Detailed MongoDB Atlas connection error:")

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
