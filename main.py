import os
from extensions import app, mongo
from models import User
from auth import auth as auth_blueprint
from flask import redirect, url_for, send_from_directory
import logging

# Set MONGO_URI environment variable
app.config['MONGO_URI'] = "mongodb+srv://servafricloud:6c3sSFoIGLgWc4wW@cluster1.9a3xw.mongodb.net/servafri_cloud?retryWrites=true&w=majority&appName=cluster1'

app.register_blueprint(auth_blueprint)

logging.basicConfig(filename='app.log', level=logging.INFO)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
