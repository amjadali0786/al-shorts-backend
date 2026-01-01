from fastapi import (
    APIRouter,
    Depends,
    Body,
    HTTPException,
    UploadFile,
    File,
    Query
)
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
import shutil

from app.core.database import SessionLocal
from app.models.news import News
from app.models.bookmark import Bookmark
from app.dependencies.admin_auth import admin_auth

# -------------------------
# ROUTER
# -------------------------
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(admin_auth)]
)

# -------------------------
# DB DEP
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# 📰 VIEW ALL NEWS (ADMIN)
# =====================================================
@router.get("/news")
def all_news(
    category: str | None = Query(None),
    language: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(News)

    if category:
        query = query.filter(News.category == category)

    if language:
        query = query.filter(News.language == language)

    if status:
        query = query.filter(News.status == status)

    return query.order_by(News.created_at.desc()).all()

# =====================================================
# ✅ APPROVE NEWS
# =====================================================
@router.post("/approve/{news_id}")
def approve_news(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    news.status = "published"
    db.commit()

    return {"message": "News approved & published"}

# =====================================================
# ❌ REJECT NEWS
# =====================================================
@router.post("/reject/{news_id}")
def reject_news(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    news.status = "rejected"
    db.commit()

    return {"message": "News rejected"}

# =====================================================
# ✏️ EDIT NEWS (FIXED)
# =====================================================
@router.put("/edit/{news_id}")
def edit_news(
    news_id: int,
    title_hi: str = Body(None),
    summary_hi: str = Body(None),
    title_en: str = Body(None),
    summary_en: str = Body(None),
    image_prompt: str = Body(None),
    db: Session = Depends(get_db)
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    if title_hi is not None:
        news.title_hi = title_hi
    if summary_hi is not None:
        news.summary_hi = summary_hi
    if title_en is not None:
        news.title_en = title_en
    if summary_en is not None:
        news.summary_en = summary_en
    if image_prompt is not None:
        news.image_prompt = image_prompt

    db.commit()
    db.refresh(news)

    return {
        "message": "News updated successfully",
        "news": news
    }

# =====================================================
# 🖼 IMAGE UPLOAD (ADMIN PREVIEW FIXED)
# =====================================================
@router.post("/upload-image/{news_id}")
def upload_image(
    news_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    upload_dir = "uploads/images"
    os.makedirs(upload_dir, exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"news_{news_id}.{ext}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔥 VERY IMPORTANT
    # This path is what admin + feed BOTH will use
    news.image_url = f"/static/images/{filename}"
    db.commit()
    db.refresh(news)

    return {
        "message": "Image uploaded successfully",
        "image_url": news.image_url
    }

# =====================================================
# 📊 ADMIN ANALYTICS OVERVIEW
# =====================================================
@router.get("/analytics/overview")
def analytics_overview(db: Session = Depends(get_db)):
    return {
        "total_news": db.query(News).count(),
        "published": db.query(News).filter(News.status == "published").count(),
        "rejected": db.query(News).filter(News.status == "rejected").count(),
        "bookmarks": db.query(Bookmark).count()
    }

# =====================================================
# 📈 NEWS-WISE ANALYTICS
# =====================================================
@router.get("/analytics/news")
def analytics_per_news(db: Session = Depends(get_db)):
    data = (
        db.query(
            News.id,
            News.title_hi,
            News.title_en,
            News.status,
            func.count(Bookmark.id).label("bookmark_count")
        )
        .outerjoin(Bookmark, Bookmark.news_id == News.id)
        .group_by(News.id)
        .all()
    )

    return [
        {
            "id": n.id,
            "title": n.title_hi or n.title_en,
            "status": n.status,
            "bookmarks": n.bookmark_count
        }
        for n in data
    ]
