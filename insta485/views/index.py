"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/', methods=["GET", "POST"])
def show_index():
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    # logname
    logname6 = ""
    if 'username' in flask.session:
        logname6 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    # getting logname
    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ?",
        (logname6,)
    )

    # getting post information
    cur = connection.execute(
        "select posts.postid, posts.owner, "
        "users.filename as user_filename, posts.filename, "
        "posts.created, count(likes.postid)as num_likes "
        "from posts "
        "left join likes on (posts.postid=likes.postid) "
        "left join users on (posts.owner=users.username) "
        "group by posts.owner, posts.filename "
        "order by posts.created DESC, posts.postid DESC"
    )
    posts = cur.fetchall()

    # get all people logname follows
    cur = connection.execute(
        "select username2 "
        "from following "
        "where username1 = ?",
        (logname6,)
    )
    following = cur.fetchall()
    logname_follows = []
    for follow in following:
        logname_follows.append(follow['username2'])
    logname_follows.append(logname6)

    for post in posts:
        if post['owner'] not in logname_follows:
            posts.remove(post)

    # get people who liked post
    for like_owners in posts:
        cur = connection.execute(
            "select owner "
            "from likes "
            "where (postid= ? and owner= ?)",
            (like_owners["postid"], logname6,)
        )
        like_owners["like_owner"] = cur.fetchall()

    # get blank like owner or awdeorio, humanize time
    updated_posts = []
    owner_time = {}
    for humanize in posts:
        owner_time = humanize["created"]
        arrow.get(owner_time)
        owner_time = arrow.utcnow()
        owner_time = owner_time.humanize()
        humanize["created"] = owner_time
        owner_time = humanize["like_owner"]
        if len(owner_time) == 0:
            owner_time = {"owner": ""}
            humanize["like_owner"] = owner_time
        updated_posts.append(humanize)

    # get user comments for each posts
    for user_comments in posts:
        cur = connection.execute(
            "select owner, text, commentid "
            "from comments "
            "where postid = ? "
            "order by created asc, commentid asc",
            (user_comments['postid'],)  # adding dictionary to a list
        )
        user_comments["comments"] = cur.fetchall()

    # Add database info to context
    context = {"logname": logname6}
    return flask.render_template("index.html", **context)
