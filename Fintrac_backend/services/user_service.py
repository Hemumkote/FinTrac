from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class UserService:
    """Service class for user-related operations."""

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def create_user(self, user_data: UserCreate) -> dict:
        """Create a new user"""
        existing_user = await self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

        # hash password

        password_hash = hash_password(user_data.password)

        user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=password_hash,
            is_active=True,
        )

        user = await self.repository.create_user(user)

        # commit transaction

        await self.session.commit()
        await self.session.refresh(user)  # ensures latest DB values

        # generate token
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

        return {"access_token": access_token, "token_type": "bearer", "user": user}

    async def login_user(self, user_login: UserLogin) -> dict:
        """Login a user"""
        user = await self.repository.get_user_by_email(user_login.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # verify password
        if not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        # generate token
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

        return {"access_token": access_token, "token_type": "bearer", "user": user}
