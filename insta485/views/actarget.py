"""
Insta485 /account/ redirect.

URLs include:
/accounts/?target=URL
"""
import os
import uuid
import pathlib
import hashlib
import flask
from flask import abort, request
import insta485


def password_hash(password, salt=uuid.uuid4().hex):
    """Hash password."""
    # create password entry
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    hash_password = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, hash_password])
    return password_db_string


def uuid_file(fileobj):
    """Create UUID for file."""
    filename = fileobj.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    return uuid_basename


def login(username, password, connection):
    """Operation login."""
    # check if name and password are empty
    if username == "" or password == "":
        abort(400)
    # check user password authentication
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    word = cur.fetchall()
    if word:
        password1 = word[0]['password']
    else:
        abort(403)
    salt = password1[7:39]
    hash_password = password_hash(password, salt)
    if hash_password != password1:
        print(hash_password)
        print(password1)
        abort(403)
    flask.session['username'] = username


def create(username, password, fullname, email, fileobj):
    """Operation create."""
    connection = insta485.model.get_db()
    if (username == "" or password == "" or
            fullname == "" or email == "" or
            fileobj == ""):
        abort(400)
    check_exist = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    exists = check_exist.fetchall()
    if len(exists) != 0:
        abort(409)
    # now creating UUID for filename and save it to disk
    uuid_basename = uuid_file(fileobj)
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    # create password entry
    password_db_string = password_hash(password)
    # add the user to database
    connection.execute(
        "INSERT INTO users "
        "(username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, fullname, email, uuid_basename, password_db_string)
    )
    # log the user in
    flask.session['username'] = username


def delete(connection):
    """Delete user."""
    # check if user is logged in
    if 'username' not in flask.session:
        abort(403)
    username = flask.session['username']
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    user_icon = cur.fetchall()
    cur2 = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner = ?",
        (username, )
    )
    post_file = cur2.fetchall()
    # delete user_icon
    for icon in user_icon:
        filename = icon['filename']
        path = insta485.app.config["UPLOAD_FOLDER"]/filename
        os.remove(path)
    # delete user_post
    for post in post_file:
        postname = post['filename']
        path = insta485.app.config["UPLOAD_FOLDER"]/postname
        os.remove(path)
    # delete user relevent infomation in database
    connection.execute(
        "DELETE FROM users "
        "WHERE username = ?",
        (username, )
    )


def edit_account(fullname, email, fileobj, connection):
    """Edit account."""
    # check if user is loged in
    if 'username' not in flask.session:
        abort(403)
    # check if fullname or email are empty
    if fullname == "" or email == "":
        abort(400)
    username = flask.session['username']
    # update fullname
    connection.execute(
        "UPDATE users SET fullname = ? "
        "WHERE username = ?",
        (fullname, username)
    )
    # update email
    connection.execute(
        "UPDATE users SET email = ? "
        "WHERE username = ?",
        (email, username)
    )
    # check if fileobj is empty
    if fileobj is None:
        return
    # update file(user_icon)
    # step one remove old file
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    names = cur.fetchall()
    filename = names[0]['filename']
    path = insta485.app.config["UPLOAD_FOLDER"]/filename
    os.remove(path)
    # step two upload new file
    uuid_basename = uuid_file(fileobj)
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    # step three update database
    connection.execute(
        "UPDATE users SET filename = ? "
        "WHERE username = ?",
        (uuid_basename, username)
    )


def update_password(password, new_password1, new_password2, connection):
    """Update password."""
    # check if user is loged in
    if 'username' not in flask.session:
        abort(403)
    # check if any fields are empty
    if password == "" or new_password1 == "" or new_password2 == "":
        abort(400)
    # verify password against user's password hashed in database
    username = flask.session['username']
    # fetch password from database
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    passwords = cur.fetchall()
    password_data = passwords[0]['password']
    salt = password_data[7:39]
    # hash input password
    password_hashed = password_hash(password, salt)
    # check if input password match database password
    if password_data != password_hashed:
        abort(403)
    # check if two new password match
    if new_password1 != new_password2:
        abort(401)
    # store password
    hashed_new = password_hash(new_password1)
    connection.execute(
        "UPDATE users SET password = ? "
        "WHERE username = ?",
        (hashed_new, username)
    )


@insta485.app.route('/accounts/', methods=['POST'])
def accounts():
    """Redirect to /accounts/?target=url."""
    # Connect to database
    connection = insta485.model.get_db()
    # get the operation
    operation = flask.request.form['operation']
    if operation == 'login':
        username = flask.request.form['username']
        password = flask.request.form['password']
        login(username, password, connection)
    elif operation == 'create':
        username = flask.request.form['username']
        password = flask.request.form['password']
        email = flask.request.form['email']
        fullname = flask.request.form['fullname']
        fileobj = flask.request.files['file']
        create(username, password, fullname, email, fileobj)
    elif operation == 'delete':
        delete(connection)
        flask.session.clear()
    elif operation == 'edit_account':
        email = flask.request.form['email']
        fullname = flask.request.form['fullname']
        fileobj = flask.request.files['file']
        edit_account(fullname, email, fileobj, connection)
    elif operation == 'update_password':
        password = flask.request.form['password']
        new_password1 = flask.request.form['new_password1']
        new_password2 = flask.request.form['new_password2']
        update_password(password, new_password1, new_password2, connection)
    # get the target and check if it exists
    target = request.args.get("target")
    if not target:
        return flask.redirect("/")
    return flask.redirect(target)
