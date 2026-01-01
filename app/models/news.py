from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)

    title_hi = Column(Text)
    summary_hi = Column(Text)

    title_en = Column(Text)
    summary_en = Column(Text)

    image_prompt = Column(Text)
    image_url = Column(Text)

    status = Column(String(20), default="draft")

    # 🔥 THIS IS THE FIX
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
