from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.cache import create_redis
from src.api.v1.exception_handler import value_error_handler
from src.api.v1.auth.auth_router import auth_router
from src.api.v1.camera.camera_router import camera_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = create_redis()

    try:
        await app.state.redis.ping()
        yield
    finally:
        await app.state.redis.aclose()

app = FastAPI(title="Camera Map API", version="1.0.0", lifespan=lifespan)
app.add_exception_handler(ValueError, value_error_handler)
app.include_router(auth_router)
app.include_router(camera_router)

@app.get("/")
async def root():
    return {"message": "Camera Map API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
