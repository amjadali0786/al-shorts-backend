from app.core.database import engine, Base

# IMPORTANT: import ALL models
from app.models.news import News
from app.models.raw_content import RawContent

Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully")
