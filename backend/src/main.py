from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.auth.auth_router import auth_router
from src.api.v1.camera.camera_router import camera_router
from src.api.v1.videos.videos_router import videos_router
from src.api.v1.users.user_routers import user_router
from src.api.v1.exception_handler import value_error_handler
from src.core.cache import create_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = create_redis()

    try:
        await app.state.redis.ping()
        yield
    finally:
        await app.state.redis.aclose()


app = FastAPI(title="Camera Map API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ValueError, value_error_handler)
app.include_router(auth_router)
app.include_router(camera_router)
app.include_router(videos_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Camera Map API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
