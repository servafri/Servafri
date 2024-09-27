from extensions import app, mongo
from models import User
from auth import auth as auth_blueprint
from flask import redirect, url_for, send_from_directory
from config import Config
import logging

app.register_blueprint(auth_blueprint)

logging.basicConfig(filename='app.log', level=logging.INFO)

# Print MongoDB URI information
Config.print_mongo_uri_info()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
