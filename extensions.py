from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config
import urllib.parse

app = Flask(__name__)
app.config.from_object(Config)

# Parse and escape MongoDB URI components
mongo_uri = app.config['MONGO_URI']
parsed_uri = urllib.parse.urlparse(mongo_uri)
username = urllib.parse.quote_plus(parsed_uri.username) if parsed_uri.username else ''
password = urllib.parse.quote_plus(parsed_uri.password) if parsed_uri.password else ''
host = parsed_uri.hostname
port = parsed_uri.port
database = parsed_uri.path.lstrip('/')

# Reconstruct the MongoDB URI with escaped components
escaped_mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/{database}"
app.config['MONGO_URI'] = escaped_mongo_uri

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.get_user_by_id(user_id)
