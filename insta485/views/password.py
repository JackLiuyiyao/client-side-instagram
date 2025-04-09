"""
Insta485 password view.

URLs include:
/acccounts/password
"""
import flask
import insta485


@insta485.app.route('/accounts/password/', methods=['GET'])
def show_password():
    """Display /accounts/password route."""
    # check if logged in
    if flask.session.get('username'):
        logname1 = flask.session['username']
    else:
        return flask.redirect(flask.url_for("show_login"))
    context = {"logname": logname1}
    return flask.render_template("password.html", **context)
