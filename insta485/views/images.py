"""
Insta485 render images.

URLs include: /uploads/<path:filename>
"""
import pathlib
import os
import flask
import insta485


@insta485.app.route('/uploads/<path:filename>')
def serve_images(filename):
    """Serve images from uploads folder."""
    if 'username' not in flask.session:
        return flask.abort(403)

    filepath = pathlib.Path(insta485.app.config['UPLOAD_FOLDER'] / filename)
    if not os.path.exists(filepath):
        return flask.abort(404)

    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)
