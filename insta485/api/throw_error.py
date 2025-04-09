"""Throws an error with message and status code."""
import flask


def throw_error(message, status_code):
    """Throw error with message and status_code."""
    return flask.jsonify({'message': message}), int(status_code)
