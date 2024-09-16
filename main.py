from extensions import app, db, login_manager, api
from models import User
from auth import auth as auth_blueprint
from api import initialize_api

app.register_blueprint(auth_blueprint)
initialize_api(api)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
