from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.news import News

router = APIRouter(prefix="/feed", tags=["Feed"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    language: str = Query("hi"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    rows = (
        db.query(News)
        .filter(News.status == "published")
        .order_by(News.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    data = []
    for n in rows:
        data.append({
            "id": n.id,
            "title_hi": n.title_hi,
            "summary_hi": n.summary_hi,
            "title_en": n.title_en,
            "summary_en": n.summary_en,
            "image_url": n.image_url,
            "created_at": n.created_at.isoformat() if n.created_at else None
        })

    return {
        "page": page,
        "limit": limit,
        "count": len(data),
        "data": data
    }
