import logging
from flask import Flask
from flask_login import LoginManager
from config import Config
import os
from flask_pymongo import PyMongo
from urllib.parse import quote_plus

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

logging.debug("Initializing extensions.py")

# Initialize PyMongo
mongo_uri = os.environ.get('MONGO_URI')
if mongo_uri:
    try:
        # Parse the URI and escape username and password
        parts = mongo_uri.split('://')
        if len(parts) == 2:
            auth_parts = parts[1].split('@')
            if len(auth_parts) == 2:
                user_pass, host_part = auth_parts
                user, password = user_pass.split(':')
                escaped_user = quote_plus(user)
                escaped_password = quote_plus(password)
                mongo_uri = f"{parts[0]}://{escaped_user}:{escaped_password}@{host_part}"

        app.config['MONGO_URI'] = mongo_uri
        mongo = PyMongo(app)
        logging.debug("MongoDB connection established successfully")
    except Exception as e:
        logging.error(f"Error initializing MongoDB connection: {str(e)}")
        mongo = None
else:
    logging.error("MONGO_URI environment variable is not set")
    mongo = None

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if mongo:
        try:
            from models import User
            user_data = mongo.db.users.find_one({"_id": user_id})
            if user_data:
                return User.from_dict(user_data)
        except Exception as e:
            logging.error(f"Error loading user: {str(e)}")
    return None

logging.debug("Finished initializing extensions.py")
