import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

logging.debug("Initializing extensions.py")

# Initialize PyMongo
mongo = PyMongo(app)

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
