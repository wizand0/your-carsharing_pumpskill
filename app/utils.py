import os
import secrets

from flask import current_app


def save_media(form_media):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_media.filename)
    media_fn = random_hex + f_ext
    media_path = os.path.join(current_app.root_path, 'static/post_media', media_fn)
    form_media.save(media_path)

    return media_fn
