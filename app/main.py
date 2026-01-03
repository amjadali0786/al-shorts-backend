from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# ROUTES
from app.routes.upload import router as upload_router
from app.routes.admin import router as admin_router
from app.routes.feed import router as feed_router
from app.auth.user_routes import router as user_auth_router
from app.routes.bookmarks import router as bookmark_router

# DB
from app.core.database import Base, engine
from app.models import user, news, bookmark  # register models

# -------------------------
# APP INIT
# -------------------------
app = FastAPI(title="AI Shorts Backend")

# -------------------------
# CORS (🔥 VERY IMPORTANT)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://al-shorts-frontend.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# STATIC FILES (SAFE)
# -------------------------
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# -------------------------
# ROUTERS
# -------------------------
app.include_router(user_auth_router)
app.include_router(upload_router)
app.include_router(admin_router)
app.include_router(feed_router)
app.include_router(bookmark_router)

# -------------------------
# DB TABLES
# -------------------------
Base.metadata.create_all(bind=engine)
