"""
Insta485 auth.

URLs include:
/acccounts/auth/
"""
import flask
from flask import abort
import insta485


@insta485.app.route('/accounts/auth/', methods=['GET'])
def show_auth():
    """Display /accounts/auth route."""
    # check if logged in
    if 'username' in flask.session:
        return ("Success", 200)
    return abort(403)
