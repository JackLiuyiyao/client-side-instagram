"""Checks if user is logged in."""
import flask
from insta485.api.throw_error import throw_error


def check_login(message, status_code):
    """Check if user is logged in."""
    username = ""
    if flask.request.authorization:
        if 'username' in flask.request.authorization:
            username = flask.request.authorization['username']
    if flask.session:
        if 'username' in flask.session:
            username = flask.session['username']

    if not username:
        return throw_error(message, status_code)
    return {'username': username}
