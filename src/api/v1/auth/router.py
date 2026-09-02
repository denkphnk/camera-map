from fastapi import APIRouter, Depends

from src.api.v1.dependencies import get_auth_service
from src.api.v1.auth.schemas import RefreshRequest, RegisterRequest, LoginRequest, TokenResponse, UserResponse
from src.domain.services.auth_service import AuthService


auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post(
    '/register',
    response_model=UserResponse
)
async def register(request: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    user = await service.register(
        email=request.email,
        full_name=request.full_name,
        password=request.password
    )
    return user


@auth_router.post(
    '/login',
    response_model=TokenResponse
)
async def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    tokens = await service.login(
        email=request.email,
        password=request.password
    )
    return tokens


@auth_router.post(
    '/refresh',
    response_model=TokenResponse
)
async def refresh(request: RefreshRequest, service: AuthService = Depends(get_auth_service)):
    tokens = await service.refresh(refresh_token=request.refresh_token)
    return tokens


@auth_router.post(
    '/logout',
    status_code=204
)
async def logout(request: RefreshRequest, service: AuthService = Depends(get_auth_service)):
    await service.logout(refresh_token=request.refresh_token)
    