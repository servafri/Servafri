from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config
import urllib.parse

app = Flask(__name__)
app.config.from_object(Config)

print("Debug: Initializing extensions.py")
mongo_uri = Config.get_mongo_uri()
print(f"Debug: Formatted MONGO_URI: {mongo_uri}")

app.config['MONGO_URI'] = mongo_uri

# Initialize PyMongo with None
mongo = None

try:
    # Attempt to create PyMongo instance
    mongo = PyMongo(app)
    
    # Test the connection
    mongo.db.command('ping')
    print("Debug: MongoDB connection established successfully")
    print("Debug: MongoDB ping successful")
except Exception as e:
    print(f"Debug: Error connecting to MongoDB: {str(e)}")
    print("Debug: Please check your MONGO_URI configuration and ensure the MongoDB Atlas cluster is accessible.")

# Only set up LoginManager if mongo connection is successful
if mongo:
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.get_user_by_id(user_id)
else:
    print("Debug: LoginManager not initialized due to MongoDB connection failure")

print("Debug: Finished initializing extensions.py")
