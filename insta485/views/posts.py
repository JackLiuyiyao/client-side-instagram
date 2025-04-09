"""
Insta485 users (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route("/posts/<postid_url_slug>/")
def show_posts(postid_url_slug):
    # Add database info to context
    """Display / route."""
    # access variable user_url_slug
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    # logname
    logname11 = ""
    if 'username' in flask.session:
        logname11 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    time = {}
    cur = connection.execute(
        "select postid from likes"
    )
    post_nums = cur.fetchall()

    posts_with_likes = []
    for post in post_nums:
        posts_with_likes.append(post['postid'])

    if int(postid_url_slug) not in posts_with_likes:
        cur = connection.execute(
            "select posts.postid, "
            "posts.owner,users.filename as users_filename, "
            "posts.created, posts.filename as posts_filename, "
            "posts.created "
            "from posts "
            "inner join users on (posts.owner=users.username) "
            "where posts.postid=?",
            (postid_url_slug,)
        )
        post_info = cur.fetchall()

        for add_info in post_info:
            cur1 = connection.execute(
                "select owner, text, commentid "
                "from comments "
                "where postid = ? "
                "order by created asc, commentid asc",
                (postid_url_slug,)
            )
            add_info["comments"] = cur1.fetchall()

            # get people who liked post
            cur = connection.execute(
                "select owner "
                "from likes "
                "where (postid= ? and owner= ?)",
                (postid_url_slug, logname11,)
            )
            add_info["like_owner"] = cur.fetchall()
            add_info["has_post"] = "no"
            time = add_info["created"]
            arrow.get(time)
            utc = arrow.utcnow()
            utc = utc.humanize()
            add_info["created"] = utc

    # get blank like owner or awdeorio, humanize time
    else:
        cur = connection.execute(
            "select posts.postid, posts.owner, "
            "users.filename as users_filename, "
            "posts.created, posts.filename as posts_filename, "
            "count(likes.postid) as num_likes, posts.created "
            "from posts "
            "inner join users on (posts.owner=users.username) "
            "inner join likes on (posts.postid=likes.postid) "
            "where posts.postid=?",
            (postid_url_slug,)
        )
        post_info = cur.fetchall()

        for add_info in post_info:
            cur2 = connection.execute(
                "select owner, text, commentid "
                "from comments "
                "where postid = ? "
                "order by created asc, commentid asc",
                (postid_url_slug,)
            )
            add_info["comments"] = cur2.fetchall()

            # get people who liked post
            cur = connection.execute(
                "select owner "
                "from likes "
                "where (postid= ? and owner= ?)",
                (postid_url_slug, logname11,)
            )
            add_info["like_owner"] = cur.fetchall()
            add_info["has_post"] = "yes"
            time = add_info["created"]
            arrow.get(time)
            utc = arrow.utcnow()
            utc = utc.humanize()
            add_info["created"] = utc

    context = {"logname": logname11, "post_info": post_info}
    return flask.render_template("posts.html", **context)
