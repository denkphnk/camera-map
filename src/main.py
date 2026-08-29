from fastapi import FastAPI

app = FastAPI(title="Camera Map API", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Camera Map API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
