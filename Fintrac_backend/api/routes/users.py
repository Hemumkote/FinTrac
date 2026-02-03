from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.models.user import User
from services.user_service import UserService
from app.db.session import get_async_session
from app.schemas.user import UserCreate, UserLogin, UserResponse


router = APIRouter(
    prefix="/api/v1/users", tags=["users"]
)  # tags is only to affect the swagger docs


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Created user successfully",
    description="Create a new user account with email and password",
)
async def register_user(
    user_create: UserCreate, session: AsyncSession = Depends(get_async_session)
) -> dict:

    service = UserService(session)
    return await service.create_user(user_create)


@router.post(
    "/login",
    response_model=UserResponse,
    status_code=201,
    summary="User Logged in successfully",
    description=" Authenticate user with email and password",
)
async def login_user(
    user_login: UserLogin, session: AsyncSession = Depends(get_async_session)
):
    service = UserService(session)
    return await service.login_user(user_login)
