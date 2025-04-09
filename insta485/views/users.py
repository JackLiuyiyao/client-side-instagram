"""
Insta485 users (main) view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route("/users/<user_url_slug>/")
def show_users(user_url_slug):
    # Add database info to context
    """Display / route."""
    # access variable user_url_slug
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    # logname
    logname12 = ""
    if 'username' in flask.session:
        logname12 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    cur = connection.execute(
        "select username "
        "from users "
        "where username not in ("
        "select owner "
        "from posts"
        ")"
    )
    no_posts = cur.fetchall()

    cur = connection.execute(
        "select username as not_following "
        "from users "
        "where username not in ("
        "select username2 "
        "from following "
        "where username1=? or username2=?"
        ")",
        (logname12, logname12,)
        )
    no_follow = cur.fetchall()

    print(no_follow)

    if user_url_slug == no_posts[0]["username"]:
        cur = connection.execute(
            "select username, fullname, filename from users where username= ?",
            (user_url_slug,)
        )
        user_profile = cur.fetchall()
        for followers in user_profile:
            # num of following
            cur = connection.execute(
                "select count(username2) as following "
                "from following "
                "where username1= ?",
                (user_url_slug,)
            )
            followers["num_following"] = cur.fetchall()

            # num followers
            cur = connection.execute(
                "select count(username1) as followers "
                "from following "
                "where username2= ?",
                (user_url_slug,)
            )
            followers["num_followers"] = cur.fetchall()

            # num of posts
            cur = connection.execute(
                "select postid, filename from posts where owner = ?",
                (user_url_slug,)
            )
            followers["posts"] = cur.fetchall()

            cur = connection.execute(
                "select following.username2 as logname_followers "
                "from following "
                "inner join users on (following.username1=users.username) "
                "where users.username= ? and following.username2= ?",
                (logname12, user_url_slug,)
            )
            followers["follower_name"] = cur.fetchall()
            followers["has_post"] = "no"
    else:
        # fullname, username, filename, num of posts
        cur = connection.execute(
            "select username, fullname, users.filename, "
            "count(posts.postid) as num_posts "
            "from posts "
            "inner join users on (users.username=posts.owner) "
            "where username=? "
            "group by username, fullname",
            (user_url_slug,)
        )
        user_profile = cur.fetchall()

        for followers in user_profile:
            # num of following
            cur = connection.execute(
                "select count(username2) as following "
                "from following "
                "where username1= ?",
                (user_url_slug,)
            )
            followers["num_following"] = cur.fetchall()

            # num followers
            cur = connection.execute(
                "select count(username1) as followers "
                "from following "
                "where username2=?",
                (user_url_slug,)
            )
            followers["num_followers"] = cur.fetchall()

            # num of posts
            cur = connection.execute(
                "select postid, filename from posts where owner = ?",
                (user_url_slug,)
            )
            followers["posts"] = cur.fetchall()

            cur = connection.execute(
                "select users.username as slug_followers "
                "from users "
                "inner join following on (users.username=following.username2) "
                "where following.username1= ?",
                (logname12,)
            )
            followers["log_following"] = cur.fetchall()

            follows = followers["log_following"]

            follow1 = []
            if no_follow:
                follow1 = no_follow[0]["not_following"]
            for follow2 in follows:
                if follow1 != follow2["slug_followers"]:
                    followers["verify"] = "no follow"
                else:
                    followers["verify"] = "follow"

            followers["has_post"] = "yes"

    context = {"logname": logname12, "user_profile": user_profile,
               "no_follows": no_follow}
    return flask.render_template("users.html", **context)
