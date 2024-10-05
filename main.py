import os
from urllib.parse import quote_plus, urlencode
import logging
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from extensions import app, login_manager, mongo
from models import User
from auth import auth as auth_blueprint

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# OAuth setup
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    api_base_url=f'https://{os.environ.get("AUTH0_DOMAIN")}',
    access_token_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/oauth/token',
    authorize_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/callback')
def callback_handling():
    logging.debug("Callback route hit")
    try:
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture'],
            'email': userinfo['email']
        }

        # Check if user exists in the database, if not, create a new user
        user = User.get_user_by_auth0_id(userinfo['sub'])
        if not user:
            new_user = User(
                username=userinfo['name'],
                email=userinfo['email'],
                auth0_id=userinfo['sub']
            )
            new_user.save()

        logging.debug("User authenticated successfully")
        return redirect(url_for('auth.dashboard'))
    except Exception as e:
        logging.error(f"Error in callback: {str(e)}")
        return jsonify(error=str(e)), 500

@app.route('/login')
def login():
    logging.debug("Login route hit")
    return auth0.authorize_redirect(redirect_uri=url_for('callback_handling', _external=True))

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': os.environ.get("AUTH0_CLIENT_ID")}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_auth0_id(user_id)

app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
