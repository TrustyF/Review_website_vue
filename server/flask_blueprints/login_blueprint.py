from functools import wraps

from flask import Blueprint, request, redirect, Response, jsonify, send_file, url_for, session
from app import oauth
import requests
import json

bp = Blueprint('login', __name__)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login.login'))

        return f(*args, **kwargs)

    return decorated


@bp.route('/')
def check():
    user = session.get('user')
    print(user)
    if user:
        return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}

    else:
        return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}


@bp.route('/login')
def login():
    return oauth.google.authorize_redirect(redirect_uri=url_for("login.authorize", _external=True))


@bp.route('/authorize', methods=["GET", "POST"])
def authorize():
    token = oauth.google.authorize_access_token()
    session['user'] = token
    return {'access_token': session.get('user')}


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.check'))
