from extensions import app, db, login_manager, api
from models import User
from auth import auth as auth_blueprint
from api import initialize_api
from flask import redirect, url_for
import logging

app.register_blueprint(auth_blueprint)
initialize_api(api)

logging.basicConfig(filename='app.log', level=logging.INFO)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000, debug=True)
