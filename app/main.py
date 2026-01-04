from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.upload import router as upload_router
from app.routes.admin import router as admin_router
from app.routes.feed import router as feed_router
from app.auth.user_routes import router as user_auth_router
from app.routes.bookmarks import router as bookmark_router

from app.core.database import Base, engine
from app.models import user, news, bookmark

app = FastAPI(title="AI Shorts Backend")

# ✅ TEMPORARY OPEN CORS (production testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 🔥 THIS FIXES FEED + ADMIN
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="uploads"), name="static")

app.include_router(upload_router)
app.include_router(admin_router)
app.include_router(feed_router)
app.include_router(user_auth_router)
app.include_router(bookmark_router)

Base.metadata.create_all(bind=engine)
