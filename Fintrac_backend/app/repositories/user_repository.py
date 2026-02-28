from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload

from app.models.user import User


class UserRepository:
    """Data access layer for the User model"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_create: User):
        """Create a new user in the DB"""
        db_user = User(
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=user_create.hashed_password,
            is_active=True,
        )
        self.session.add(db_user)  # Add user to session
        await self.session.flush()  # Flush to get the ID assigned, Id will get generated
        return db_user

    async def get_user_by_email(self, email: str) -> User | None:
        """Retrieve a user by email"""
        result = await self.session.execute(select(User).where(User.email == email))
        return (
            result.scalar_one_or_none()
        )  ## scalar is to extract the first column of the first row or None if no rows

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by ID"""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_with_relations(self, user_id: int) -> User | None:
        """Retrieve a user by ID with profile and settings eagerly loaded"""
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.profile), selectinload(User.settings))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_user(self, user: User) -> User:
        """Update user information in the DB"""
        self.session.add(user)  # Add updated user to session
        await self.session.flush()  # Flush to apply changes
        return user
