from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.bookmark import Bookmark
from app.models.news import News
from app.dependencies.user_auth import get_current_user

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# GET USER BOOKMARKS ✅
# -------------------------
@router.get("/")
def user_bookmarks(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(News)
        .join(Bookmark, Bookmark.news_id == News.id)
        .filter(Bookmark.user_id == user.id)
        .all()
    )

# -------------------------
# TOGGLE BOOKMARK ✅
# -------------------------
@router.post("/{news_id}")
def toggle_bookmark(
    news_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    bookmark = (
        db.query(Bookmark)
        .filter(
            Bookmark.user_id == user.id,
            Bookmark.news_id == news_id
        )
        .first()
    )

    if bookmark:
        db.delete(bookmark)
        db.commit()
        return {"bookmarked": False}

    new_bm = Bookmark(user_id=user.id, news_id=news_id)
    db.add(new_bm)
    db.commit()

    return {"bookmarked": True}
