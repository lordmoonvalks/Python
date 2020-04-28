import os
import secrets
from flask import current_app

#saving files uploaded to to local static fodler
def save_file(file):
    random_hex = secrets.token_hex(8)
    _, f_ext, = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/files',
                             file_fn)
    file.save(file_path)
    return file_fn
