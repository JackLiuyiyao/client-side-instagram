"""
Insta485 all endpoints that only accept post requests.

URLs include:
/following/?target=URL
/likes/?target=URL
/comments/?target=URL
/posts/?target=URL
"""
import pathlib
import uuid
import os
import flask
import insta485


@insta485.app.route('/following/', methods=['POST'])
def follow_unfollow_user():
    """Update the follow table for this user."""
    redirect_to = flask.request.args.get("target")
    if not redirect_to:
        redirect_to = '/'

    operation = flask.request.form.get("operation")

    # Connect to database
    connection = insta485.model.get_db()
    logname7 = ""
    if 'username' in flask.session:
        logname7 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')
    # person logname is trying to follow
    username = flask.request.form.get("username")
    print(username)

    cur = connection.execute(
        "SELECT username1, username2 "
        "FROM following "
        "WHERE username1 = ?",
        (logname7,)
    )
    following = cur.fetchall()
    following_list = []

    for user in following:
        following_list.append(user['username2'])
    print(following_list)

    if operation == "follow":
        if username in following_list:
            flask.abort(409)
        # Query database
        connection.execute(
            "INSERT INTO following(username1, username2) "
            "VALUES (?, ?)",
            (logname7, username)
        )

        cur = connection.execute(
            "SELECT username1, username2 "
            "FROM following "
            "WHERE username1 = ?",
            (logname7,)
        )
        following = cur.fetchall()
        print(following)
    elif operation == "unfollow":
        if username not in following_list:
            flask.abort(409)
        connection.execute(
            "DELETE FROM following "
            "WHERE username1 = ? AND username2 = ?",
            (logname7, username)
        )
    return flask.redirect(redirect_to)


@insta485.app.route('/likes/', methods=['POST'])
def update_likes():
    """Update the likes table for certain post."""
    redirect_to = flask.request.args.get("target")
    if not redirect_to:
        redirect_to = '/'

    operation = flask.request.form.get("operation")

    # Connect to database
    connection = insta485.model.get_db()
    logname8 = ""
    if 'username' in flask.session:
        logname8 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    postid = int(flask.request.form.get("postid"))
    print("POST ID IS", postid)
    cur = connection.execute(
        "SELECT postid  "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (logname8, postid)
    )
    owner_likes = cur.fetchall()
    owner_likes_list = []

    for like in owner_likes:
        owner_likes_list.append(like['postid'])
    print("What is in postidish", owner_likes)
    print("owner_likes_list:", owner_likes_list)

    cur = connection.execute(
        "select posts.postid, "
        "count(likes.postid)as num_likes "
        "from posts "
        "inner join likes on (posts.postid=likes.postid) "
        "where likes.postid= ? "
        "group by posts.postid "
        "order by posts.postid DESC",
        (postid,)
    )

    likes_num = cur.fetchall()
    likes_num_list = []

    for like_amount in likes_num:
        likes_num_list.append(like_amount["num_likes"])
    print("amount of likes is ", likes_num_list)

    if operation == "like":
        if postid in owner_likes_list:
            flask.abort(409)
        # Query database
        connection.execute(
            "INSERT INTO likes(owner, postid) "
            "VALUES (?, ?)",
            (logname8, postid)
        )
    elif operation == "unlike":
        if postid not in owner_likes_list:
            flask.abort(409)

        if likes_num_list == 1:
            connection.execute(
                "DELETE FROM likes "
                "WHERE owner = ? AND postid = ?",
                (logname8, postid)
            )

        connection.execute(
                "DELETE FROM likes "
                "WHERE owner = ? AND postid = ?",
                (logname8, postid)
            )
    return flask.redirect(redirect_to)


@insta485.app.route('/comments/', methods=['POST'])
def update_comments():
    """Update the comments table for certain post."""
    redirect_to = flask.request.args.get("target")
    if not redirect_to:
        redirect_to = '/'

    # Connect to database
    connection = insta485.model.get_db()
    logname9 = ""
    if 'username' in flask.session:
        logname9 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    print(flask.request.form)
    operation = flask.request.form.get("operation")
    postid = flask.request.form.get("postid")
    text = flask.request.form.get("text")

    cur = connection.execute(
        "SELECT commentid "
        "FROM comments "
        "WHERE owner = ?",
        (logname9,)
    )
    owner_comments = cur.fetchall()
    owner_comments_list = []

    for comment in owner_comments:
        owner_comments_list.append(comment['commentid'])

    if operation == "create":
        if len(text) == 0:
            flask.abort(400)
        # Query database
        print(logname9, postid, text)
        connection.execute(
            "INSERT INTO comments(owner, postid, text) "
            "VALUES (?, ?, ?)",
            (logname9, postid, text)
        )
    elif operation == "delete":
        commentid = int(flask.request.form.get("commentid"))
        if commentid not in owner_comments_list:
            flask.abort(403)
        connection.execute(
            "DELETE FROM comments "
            "WHERE commentid = ?",
            (commentid,)
        )
    return flask.redirect(redirect_to)


@insta485.app.route('/posts/', methods=['POST'])
def update_posts():
    """Update the posts table."""
    logname10 = ""
    if 'username' in flask.session:
        logname10 = flask.session['username']
    else:
        return flask.redirect('/accounts/login/')

    redirect_to = flask.request.args.get("target")
    if not redirect_to:
        redirect_to = f'/users/{logname10}/'

    # Connect to database
    connection = insta485.model.get_db()

    operation = flask.request.form.get("operation")

    if operation == "create":
        # Unpack flask object
        fileobj = flask.request.files["file"]
        if not fileobj:
            flask.abort(400)

        filename = fileobj.filename

        # Compute base name (filename without directory).
        # We use a UUID to avoid clashes with existing files,
        # and ensure that the name is compatible with the
        # filesystem. For best practive, we ensure uniform
        # file extensions (e.g. lowercase).
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        # Query database
        connection.execute(
            "INSERT INTO posts(filename, owner) "
            "VALUES (?, ?)",
            (uuid_basename, logname10)
        )
    elif operation == "delete":
        postid = flask.request.form.get("postid")
        print(postid)
        cur = connection.execute(
            "SELECT filename FROM posts "
            "WHERE postid = ?",
            (postid,)
        )
        filename = cur.fetchall()

        os.remove(
            os.path.join(insta485.app.config["UPLOAD_FOLDER"],
                         filename[0]['filename']))

        connection.execute(
            "DELETE FROM posts "
            "WHERE postid = ?",
            (postid,)
        )
    return flask.redirect(redirect_to)
