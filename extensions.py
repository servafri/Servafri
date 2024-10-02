import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

logging.debug("Initializing extensions.py")

# Initialize PyMongo
try:
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")
    app.config['MONGO_URI'] = mongo_uri
    mongo = PyMongo(app)
    mongo.db.command('ping')
    logging.info("MongoDB connection successful")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {str(e)}")
    logging.exception("Detailed MongoDB connection error:")

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({"_id": user_id})
        if user_data:
            from models import User
            return User.from_dict(user_data)
    except Exception as e:
        logging.error(f"Error loading user: {str(e)}")
        logging.exception("Detailed user loading error:")
    return None

logging.debug("Finished initializing extensions.py")
