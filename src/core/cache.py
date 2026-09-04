from fastapi import Request
from redis.asyncio import Redis

from src.core.config import settings


def create_redis() -> Redis:
    redis = Redis.from_url(url=str(settings.REDIS_URL), decode_responses=True)

    return redis


def get_redis(request: Request) -> Redis:
    return request.app.state.redis