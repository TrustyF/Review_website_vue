from functools import wraps

from flask import Blueprint, request, redirect, Response, jsonify, send_file, url_for, session
import json

from constants import FIREBASE_ADMIN_UID

bp = Blueprint('login', __name__)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        id_token = request.headers.get('Authorization')

        if id_token != FIREBASE_ADMIN_UID:
            return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}

        return f(*args, **kwargs)

    return decorated


@bp.route('/verify', methods=["GET", "POST"])
@requires_auth
def verify():
    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}
