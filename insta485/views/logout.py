"""
Insta485 logout.

URLs include:
/accounts/logout/
"""
import flask
import insta485


@insta485.app.route('/accounts/logout/', methods=['POST'])
def show_logout():
    """Log user out."""
    flask.session.clear()
    return flask.redirect(flask.url_for("show_login"))
