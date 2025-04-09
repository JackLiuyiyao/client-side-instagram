"""
Insta485 users (main) view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route("/users/<user_url_slug>/following/")
def show_following(user_url_slug):
    # Add database info to context
    """Display / route."""
    # access variable user_url_slug
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    # logname
    logname4 = ""
    if 'username' in flask.session:
        logname4 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    cur = connection.execute(
        "select users.username, users.filename "
        "from users "
        "inner join following on (users.username=following.username2) "
        "where following.username1=?",
        (user_url_slug,)
    )
    following_info = cur.fetchall()

    print(following_info)

    context = {"logname": logname4, "following_info": following_info,
               "username": user_url_slug}
    return flask.render_template("following.html", **context)
