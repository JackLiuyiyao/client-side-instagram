"""
Insta485 explore view.

URLs include:
/explore/
"""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """Display /explore route."""
    logname2 = ""
    if 'username' in flask.session:
        logname2 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT users.username, filename "
        "FROM users "
        "JOIN ("
        "SELECT username "
        "FROM users "
        "WHERE username != ? "
        "EXCEPT "
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?"
        ") v "
        "ON users.username = v.username",
        (logname2, logname2)
    )
    users = cur.fetchall()
    print(users)

    # Add database info to context
    context = {"logname": logname2, "not_following": users}
    return flask.render_template("explore.html", **context)
