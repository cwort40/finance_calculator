from flask import Blueprint, redirect, url_for, session, request, render_template
from functools import wraps
from flask_oauthlib.client import OAuth
import os

auth = Blueprint('auth', __name__)

oauth = OAuth(auth)

google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('YOUR_GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('YOUR_GOOGLE_CLIENT_SECRET'),
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/userinfo',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@auth.route('/login')
def login():
    return render_template('login.html', show_modal=False)  # Render the login page


@auth.route('/google_login')
def google_login():
    return google.authorize(callback=url_for('auth.login_callback', _external=True))


@auth.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('home'))  # Redirect to your home route


@auth.route('/login/callback')
def login_callback():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        # Handle login error
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    session['user'] = user_info.data  # You can store user info in session

    return redirect(url_for('home'))  # Redirect to the home route


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')



