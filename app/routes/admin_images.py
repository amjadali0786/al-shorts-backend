from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.news import News
from app.dependencies.admin_auth import admin_auth
import os
import shutil

router = APIRouter(
    prefix="/admin",
    tags=["Admin Images"],
    dependencies=[Depends(admin_auth)]
)

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-image/{news_id}")
def upload_news_image(
    news_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        return {"error": "News not found"}

    filename = f"news_{news_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    news.image_url = f"/uploads/images/{filename}"
    db.commit()

    return {
        "message": "Image uploaded successfully",
        "image_url": news.image_url
    }
