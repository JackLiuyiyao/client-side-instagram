"""
Insta485 edit view.

URLs include:
/acccounts/edit
"""
import flask
import insta485


@insta485.app.route('/accounts/edit/', methods=['GET'])
def show_edit():
    """Display /accounts/edit route."""
    logname1 = ""
    # check if logged in
    if flask.session.get('username'):
        logname1 = flask.session['username']
    else:
        return flask.redirect(flask.url_for("show_login"))
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT fullname, email, filename "
        "FROM users "
        "WHERE username = ?",
        (logname1,)
    )
    content = cur.fetchall()
    file_name = content[0]['filename']
    owner_img_url = insta485.app.config["UPLOAD_FOLDER"]/file_name
    fullname = content[0]['fullname']
    email = content[0]['email']
    context = {"logname": logname1, "fullname": fullname, "email": email,
               "owner_img_url": owner_img_url}
    return flask.render_template("edit.html", **context)
