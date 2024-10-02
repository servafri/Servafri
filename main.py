import os
from extensions import app, mongo
from models import User
from auth import auth as auth_blueprint
from flask import redirect, url_for, send_from_directory
import logging
from urllib.parse import quote_plus

# Set MONGO_URI environment variable with properly escaped username and password
username = quote_plus('servafricloud')
password = quote_plus('6c3sSFoIGLgWc4wW')
os.environ['MONGO_URI'] = f'mongodb+srv://{username}:{password}@cluster1.9a3xw.mongodb.net/?retryWrites=true&w=majority&appName=cluster1'

app.register_blueprint(auth_blueprint)

logging.basicConfig(filename='app.log', level=logging.INFO)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/index')
def serve_index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
