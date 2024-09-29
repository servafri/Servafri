import logging
from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

logging.debug("Initializing extensions.py")
logging.debug(f"MONGO_URI: {app.config['MONGO_URI']}")

# Initialize PyMongo
mongo = PyMongo(app)

try:
    # Test the connection
    mongo.db.command('ping')
    logging.info("MongoDB connection established successfully")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {str(e)}")
    logging.error(f"MONGO_URI: {app.config['MONGO_URI']}")
    mongo = None

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
        return None

logging.debug("Finished initializing extensions.py")
