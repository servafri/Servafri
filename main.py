from flask_migrate import Migrate
from extensions import app, db
from models import User
from auth import auth as auth_blueprint
from flask import redirect, url_for
import logging

app.register_blueprint(auth_blueprint)

logging.basicConfig(filename='app.log', level=logging.INFO)

migrate = Migrate(app, db)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
