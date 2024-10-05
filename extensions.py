import logging
from flask import Flask
from flask_login import LoginManager
from config import Config
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)

logging.debug("Initializing extensions.py")

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # We'll need to implement a way to load users without MongoDB
    # For now, we'll return None
    return None

logging.debug("Finished initializing extensions.py")
