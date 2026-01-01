from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os
import uuid

from app.core.database import SessionLocal
from app.models.raw_content import RawContent
from app.workers.ai_pipeline import process_content
from app.utils.text_extractor import extract_text

router = APIRouter(prefix="/upload", tags=["Upload"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # -------------------------
    # SAVE FILE TEMPORARILY
    # -------------------------
    os.makedirs("uploads/raw", exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    temp_name = f"{uuid.uuid4()}{ext}"
    temp_path = os.path.join("uploads/raw", temp_name)

    with open(temp_path, "wb") as f:
        f.write(file.file.read())

    # -------------------------
    # EXTRACT TEXT (REAL CONTENT)
    # -------------------------
    extracted_text = extract_text(temp_path)

    print("📄 FILE NAME:", file.filename)
    print("📄 FILE SIZE:", len(extracted_text))
    print("📄 FILE CONTENT (FIRST 500 CHARS):")
    print(extracted_text[:500])

    if not extracted_text.strip():
        return {"error": "No readable text found in file"}

    # -------------------------
    # SAVE RAW CONTENT
    # -------------------------
    content = RawContent(
        filename=file.filename,
        file_type=file.content_type,
        text_content=extracted_text,
        status="processed"
    )

    db.add(content)
    db.commit()
    db.refresh(content)

    # -------------------------
    # AI PIPELINE (PASS REAL TEXT)
    # -------------------------
    process_content(content)

    return {"message": "File uploaded & processed successfully"}
