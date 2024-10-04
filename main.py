import os
from urllib.parse import quote_plus
import logging
from extensions import app, mongo
from models import User
from auth import auth as auth_blueprint
from flask import redirect, url_for, send_from_directory

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Set MONGO_URI environment variable
username = quote_plus('servafricloud')
password = quote_plus('6c3sSFoIGLgWc4wW')
os.environ['MONGO_URI'] = f'mongodb+srv://{username}:{password}@cluster1.9a3xw.mongodb.net/servafri_cloud?retryWrites=true&w=majority'

app.register_blueprint(auth_blueprint)

# Initialize MongoDB connection
with app.app_context():
    try:
        mongo.db.command('ping')
        logging.debug("MongoDB connection successful")
    except Exception as e:
        logging.error(f"MongoDB connection failed: {str(e)}")

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
