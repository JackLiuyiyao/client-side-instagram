"""
Insta485 users (main) view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route("/users/<user_url_slug>/followers/")
def show_followers(user_url_slug):
    # Add database info to context
    """Display / route."""
    # access variable user_url_slug
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    # logname
    logname3 = ""
    if 'username' in flask.session:
        logname3 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    # Everyone who follows logname
    cur = connection.execute(
        "SELECT users.username, users.filename "
        "FROM users "
        "JOIN following ON (users.username = following.username1) "
        "WHERE following.username2 = ?",
        (logname3,)
    )
    follower_info = cur.fetchall()

    # Everyone logname follows
    cur = connection.execute(
        "SELECT username2 as username "
        "FROM following "
        "WHERE username1 = ?",
        (logname3,)
    )
    following = cur.fetchall()
    print(following)

    for follower in follower_info:
        for follow in following:
            if follower['username'] == follow['username']:
                follower['logname_follows'] = True
    print(follower_info)

    context = {"logname": logname3, "follower_info": follower_info,
               "username": user_url_slug}
    return flask.render_template("followers.html", **context)
