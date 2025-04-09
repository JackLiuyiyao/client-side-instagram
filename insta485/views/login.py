"""
Insta485 login view.

URLs include:
/acccounts/login
"""
import flask
import insta485


@insta485.app.route('/accounts/login/', methods=['GET'])
def show_login():
    """Display /accounts/login route."""
    # check if logged in
    if flask.session.get('username'):
        return flask.redirect(flask.url_for("show_index"))
    context = {"text": "link to home"}
    return flask.render_template("login.html", **context)
