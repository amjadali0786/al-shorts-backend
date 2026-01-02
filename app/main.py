from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
        "http://localhost:5173",   # local dev
        "https://al-shorts-frontend-itqu8lv9u-amjad-alis-projects-82e9b039.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# STATIC FILES
# -------------------------
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# -------------------------
# ROUTERS
# -------------------------
app.include_router(upload_router)
app.include_router(admin_router)
app.include_router(feed_router)
app.include_router(user_auth_router)
app.include_router(bookmark_router)

# -------------------------
# DB TABLES
# -------------------------
Base.metadata.create_all(bind=engine)
