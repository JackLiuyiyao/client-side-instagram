"""
Insta485 create view.

URLs include:
/acccounts/create
"""
import flask
import insta485


@insta485.app.route('/accounts/create/', methods=['GET'])
def show_create():
    """Display /accounts/create route."""
    # check if logged in
    if flask.session.get('username'):
        return flask.redirect(flask.url_for("show_edit"))
    context = {"text": "Link to Home"}
    return flask.render_template("create.html", **context)
