from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.database import Base

class RawContent(Base):
    __tablename__ = "raw_contents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(300))
    file_type = Column(String(150))   # IMPORTANT
    text_content = Column(Text, nullable=True)
    file_path = Column(String(500))
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
