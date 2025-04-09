"""Insta485 model (database) API."""
import sqlite3
import flask
import insta485


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = insta485.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@insta485.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


# create new like
def create_like(username, postid_url_slug):
    """Create a new like in the database."""
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO likes(owner, postid) "
        "VALUES (?, ?)",
        (username, postid_url_slug,)
    )
    connection.commit()

    like = connection.execute(
        "select likeid from likes where owner=? order by likeid DESC",
        (username,)
    )
    like = like.fetchone()

    new_user = {}
    new_user["likeid"] = like["likeid"]
    new_user['url'] = f"/api/v1/likes/{like['likeid']}/"

    return flask.jsonify(new_user)


# create new comment
def create_comment(username, postid_url_slug, text):
    """Create a new commnt in the database."""
    connection = insta485.model.get_db()
    connection.execute(
        "insert into comments(owner, postid, text)"
        "values(?,?,?)",
        (username, postid_url_slug, text,)
    )

    comment = connection.execute(
        "select commentid, text "
        "from comments "
        "where owner=? and postid=? "
        "order by commentid DESC",
        (username, postid_url_slug)
    )
    comment = comment.fetchone()
    new_comment = {}
    new_comment["commentid"] = comment['commentid']
    new_comment["lognameOwnsThis"] = True
    new_comment["owner"] = username
    new_comment["ownerShowUrl"] = f"/users/{username}/"
    new_comment["text"] = comment["text"]
    new_comment['url'] = f"/api/v1/comments/{comment['commentid']}/"

    return flask.jsonify(new_comment)
