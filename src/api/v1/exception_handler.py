from fastapi import Request
from fastapi.responses import JSONResponse


async def value_error_handler(request: Request, exc: ValueError):
    message = str(exc)

    if "already exists" in message:
        status_code = 409
    elif "not found" in message:
        status_code = 404
    else:
        status_code = 401

    return JSONResponse(
        status_code=status_code,
        content={"detail": message},
    )