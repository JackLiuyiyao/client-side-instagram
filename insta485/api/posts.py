"""REST API for posts."""
import flask
import insta485
from insta485.api.check_login import check_login
from insta485.api.throw_error import throw_error


@insta485.app.route('/api/v1/posts/')
def get_ten_posts():
    """Return latest 10 posts."""
    logname = check_login("You are not logged in.", 403)
    if 'username' not in logname:
        return logname
    username = logname['username']

    connection = insta485.model.get_db()

    max_num_posts = connection.execute(
        "select max(postid) as postid "
        "from posts "
        "where owner in "
        "(select username2 "
        "from following "
        "where username1 = ? or username2 = ? "
        "group by username2)",
        (username, username)
    )
    max_num_posts = max_num_posts.fetchone()
    max_num_posts = max_num_posts['postid']
    postid_lte = max_num_posts

    if 'postid_lte' in flask.request.args:
        postid_lte = flask.request.args.get("postid_lte")

    # limit = size
    size = flask.request.args.get("size", default=10, type=int)
    if size < 0:
        return throw_error("Bad Request", 400)

    # num pages = max number of posts / size
    page = flask.request.args.get("page", default=0, type=int)
    if page < 0:
        return throw_error("Bad Request", 400)

    offset = size * page

    result = {}

    posts = connection.execute(
        "select postid "
        "from posts "
        "where owner in "
        "(select username2 "
        "from following "
        "where username1 = ? or username2 = ? "
        "group by username2) "
        "and postid <= ? "
        "order by postid desc "
        "limit ? "
        "offset ?",
        (username, username, postid_lte, size, offset)
    )
    result['results'] = posts.fetchall()

    request_size = len(result['results'])
    if request_size < size:
        result['next'] = ""
    else:
        result['next'] = (f"/api/v1/posts/?size={size}"
                          f"&page={page+1}&postid_lte={postid_lte}")

    for post in result['results']:
        post['url'] = f"/api/v1/posts/{post['postid']}/"

    if flask.request.query_string:
        result['url'] = flask.request.full_path
    else:
        result['url'] = flask.request.path
    return flask.jsonify(result)


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid."""
    logname = check_login("You are not logged in.", 403)
    if 'username' not in logname:
        return logname
    username = logname['username']

    connection = insta485.model.get_db()

    result = {}

    # post info
    post = connection.execute(
       "select * "
       "from posts "
       "where postid = ?",
       (postid_url_slug,)
    )
    post = post.fetchone()
    if not post:
        return throw_error("Not Found", 404)

    result["created"] = post["created"]
    result["imgUrl"] = f"/uploads/{post['filename']}"
    result['owner'] = post['owner']
    result["ownerShowUrl"] = f"/users/{post['owner']}/"
    result['postid'] = post['postid']
    result['postShowUrl'] = f"/posts/{post['postid']}/"
    result['url'] = f"/api/v1/posts/{post['postid']}/"

    # post comments
    comments = connection.execute(
       "select commentid, owner, text "
       "from comments "
       "where postid = ?",
       (postid_url_slug,)
    )
    comments = comments.fetchall()

    for comment in comments:
        if comment['owner'] == username:
            comment['lognameOwnsThis'] = True
        else:
            comment['lognameOwnsThis'] = False
        comment['ownerShowUrl'] = f"/users/{comment['owner']}/"
        comment['url'] = f"/api/v1/comments/{comment['commentid']}/"

    result["comments"] = comments
    result["comments_url"] = f"/api/v1/comments/?postid={postid_url_slug}"

    # post likes
    result['likes'] = {
        'lognameLikesThis': False,
        'numLikes': 0,
        'url': None
    }
    likes = connection.execute(
       "select likeid, owner "
       "from likes "
       "where postid = ?",
       (postid_url_slug,)
    )
    likes = likes.fetchall()

    for like in likes:
        result['likes']['numLikes'] += 1
        if like['owner'] == username:
            result['likes']['lognameLikesThis'] = True
            result['likes']['url'] = f"/api/v1/likes/{like['likeid']}/"

    # post owner file
    owner_file = connection.execute(
       "select filename "
       "from users "
       "where username = ?",
       (result['owner'],)
    )
    owner_file = owner_file.fetchone()

    result['ownerImgUrl'] = f"/uploads/{owner_file['filename']}"
    # print("The results are:", result)
    return flask.jsonify(result)


# new like
@insta485.app.route('/api/v1/likes/', methods=['POST'])
def post_likes():
    """Return post on postid."""
    username = check_login("You are not logged in.", 403)
    if 'username' not in username:
        return username
    username = username['username']
    postid_url_slug = flask.request.args.get("postid")
    connection = insta485.model.get_db()
    model = insta485.model

    result = {}
    # get likeid for postid and awdeorio
    like = connection.execute(
        "select likeid "
        "from likes "
        "where owner=? and postid=? "
        "order by likeid DESC",
        (username, postid_url_slug)
    )
    like = like.fetchone()

    if like:
        result["likeid"] = like["likeid"]
        result['url'] = f"/api/v1/likes/{like['likeid']}/"

        return flask.jsonify(result), 200

    # if like does not already exist return
    return model.create_like(username, postid_url_slug), 201


# new comment
@insta485.app.route('/api/v1/comments/', methods=['POST'])
def post_comments():
    """Return post on postid."""
    username = check_login("You are not logged in.", 403)
    if 'username' not in username:
        return username
    username = username['username']
    text = flask.request.json.get("text", None)
    postid_url_slug = flask.request.args.get("postid")
    model = insta485.model

    # if like does not already exist return 201 = Created
    return model.create_comment(username, postid_url_slug, text), 201
