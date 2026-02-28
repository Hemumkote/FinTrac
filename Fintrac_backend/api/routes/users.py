from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.common import APIResponse
from app.dependencies import get_current_user
from app.models.user import User
from services.user_service import UserService
from app.db.session import get_async_session
from app.schemas.user import (
    LoginResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)


router = APIRouter(
    prefix="/api/v1/user", tags=["user"]
)  # tags is only to affect the swagger docs


@router.post(
    "/register",
    response_model=APIResponse[UserResponse],
    status_code=201,
    summary="Created user successfully",
    description="Create a new user account with email and password",
)
async def register_user(
    user_create: UserCreate, session: AsyncSession = Depends(get_async_session)
) -> APIResponse[UserResponse]:

    service = UserService(session)
    user = await service.create_user(user_create)
    return APIResponse.created(
        status=201, data=user, message="User created successfully"
    )


@router.post(
    "/login",
    response_model=APIResponse[LoginResponse],
    status_code=201,
    summary="User Logged in successfully",
    description=" Authenticate user with email and password",
)
async def login_user(
    user_login: UserLogin, session: AsyncSession = Depends(get_async_session)
) -> APIResponse[LoginResponse]:
    service = UserService(session)
    post_login_data = await service.login_user(user_login)
    return APIResponse.ok(
        data=post_login_data, message="Logged in successfully", status=200
    )


@router.get(
    "/get-user-by-email",
    response_model=APIResponse[UserResponse],
    status_code=200,
    summary="Get user by email",
)
async def get_user_by_email(
    email: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> APIResponse[UserResponse]:
    print(f"Requested email: {email}, Current user email: {current_user.email}")
    if email != current_user.email:
        raise HTTPException(status_code=403, detail="Access denied")
    service = UserService(session)
    user_data = await service.get_user_by_email(current_user)
    return APIResponse.ok(
        data=user_data, message="User data fetched successfully", status=200
    )


@router.put(
    "/update-profile",
    response_model=APIResponse[UserResponse],
    status_code=200,
    summary="Update user profile",
    description="Update user profile information and preferences",
)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> APIResponse[UserResponse]:
    print(
        f"Updating user profile for user ID: {user_update.id}, email: {user_update.email}. Current user ID: {current_user.id}, email: {current_user.email}"
    )
    if current_user.id != user_update.id or current_user.email != user_update.email:
        raise HTTPException(status_code=403, detail="Access denied")
    service = UserService(session)
    updated_user_data = await service.update_user_profile(user_update)
    return APIResponse.ok(
        data=updated_user_data, message="User updated successfully", status=200
    )
