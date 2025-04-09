"""REST API for delete."""
import insta485
from insta485.api.throw_error import throw_error
from insta485.api.check_login import check_login


@insta485.app.route('/api/v1/likes/<int:likeid_slug>/', methods=["DELETE"])
def delete_like(likeid_slug):
    """Delete one like."""
    username = check_login("You are not logged in.", 403)
    if 'username' not in username:
        return username
    username = username['username']
    connection = insta485.model.get_db()
    like = connection.execute(
      "SELECT owner "
      "FROM likes "
      "WHERE likeid=?",
      (likeid_slug, )
    )
    like = like.fetchone()
    if not like:
        return throw_error("Like not found", 404)
    if username != like["owner"]:
        return throw_error("Action forbidden", 403)
    connection.execute(
      "DELETE FROM likes "
      "WHERE likeid=?",
      (likeid_slug, )
    )
    return throw_error("Like deleted", 204)


@insta485.app.route('/api/v1/comments/<int:commentid_slug>/',
                    methods=["DELETE"])
def delete_comment(commentid_slug):
    """Delete one comment."""
    username = check_login("You are not logged in.", 403)
    if 'username' not in username:
        return username
    username = username['username']
    connection = insta485.model.get_db()
    comment = connection.execute(
      "SELECT owner "
      "FROM comments "
      "WHERE commentid=?",
      (commentid_slug, )
    )
    comment = comment.fetchone()
    if not comment:
        return throw_error("Comment not found", 404)
    if username != comment["owner"]:
        return throw_error("Action forbidden", 403)
    connection.execute(
      "DELETE FROM comments "
      "WHERE commentid=?",
      (commentid_slug, )
    )
    return throw_error("Comment deleted", 204)
