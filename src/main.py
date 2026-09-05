from fastapi import FastAPI

from src.api.v1.exception_handler import value_error_handler
from api.v1.auth.auth_router import auth_router

app = FastAPI(title="Camera Map API", version="1.0.0")
app.add_exception_handler(ValueError, value_error_handler)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Camera Map API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
