from fastapi import UploadFile
import shutil
import os
import uuid

# -------------------------
# BASE UPLOAD DIR
# -------------------------
BASE_UPLOAD_DIR = "uploads"
FILES_DIR = os.path.join(BASE_UPLOAD_DIR, "files")

os.makedirs(FILES_DIR, exist_ok=True)


def save_file(file: UploadFile) -> str:
    """
    Save any uploaded file safely and return file path
    """

    # ✅ unique filename (no overwrite issue)
    ext = os.path.splitext(file.filename)[1]
    safe_name = f"{uuid.uuid4().hex}{ext}"

    file_path = os.path.join(FILES_DIR, safe_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path
