from fastapi import APIRouter, HTTPException, status, Depends

from src.domain.services.user_service import UserService
from src.data.models.user_model import User
from src.api.v1.users.user_schemas import UserProfileResponse, UserUpdateRequest

from src.api.v1.dependencies import get_user_service, get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/me", response_model=UserProfileResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    profile = await service.get_me(current_user.id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return profile

@user_router.patch("/me", response_model=UserProfileResponse)
async def update_me(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    profile = await service.update_me(current_user.id, data)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return profile