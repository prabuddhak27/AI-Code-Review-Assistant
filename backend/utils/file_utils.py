import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

IGNORED_DIR_NAMES = {"node_modules", "venv", ".venv", "__pycache__", ".git", "dist", "build"}


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file_storage) -> str:
    """Saves an uploaded file to a unique path inside UPLOAD_FOLDER and returns the path."""
    filename = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    dest_dir = current_app.config["UPLOAD_FOLDER"]
    dest_path = os.path.join(dest_dir, unique_name)
    file_storage.save(dest_path)
    return dest_path


def should_skip_path(path: str) -> bool:
    parts = set(path.split(os.sep))
    return bool(parts & IGNORED_DIR_NAMES)
