"""
Insta485 delete view.

URLs include:
/acccounts/delete
"""
import flask
import insta485


@insta485.app.route('/accounts/delete/', methods=['GET'])
def show_delete():
    """Display /accounts/delete route."""
    # check if logged in
    if flask.session.get('username'):
        logname = flask.session['username']
    else:
        return flask.redirect(flask.url_for("show_login"))
    context = {"logname": logname}
    return flask.render_template("delete.html", **context)
