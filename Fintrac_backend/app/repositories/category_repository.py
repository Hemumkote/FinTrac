from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryRepository:
    """Repository for reading predefined categories from the database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_category_by_id(self, category_id: int) -> Category | None:
        """Retrieve a category by its ID."""
        result = await self.session.execute(
            select(Category).where(
                Category.id == category_id,
                Category.is_active == True,
            )
        )
        return result.scalar_one_or_none()

    async def get_all_categories(
        self, type: str | None = None
    ) -> Sequence[Category]:
        """Retrieve all active predefined categories, optionally filtered by type."""
        query = select(Category).where(Category.is_active == True)
        if type:
            query = query.where(Category.type == type)
        query = query.order_by(Category.type, Category.name)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_category_by_name_and_type(
        self, name: str, type: str
    ) -> Category | None:
        """Retrieve a category by its name and type."""
        result = await self.session.execute(
            select(Category).where(
                Category.name == name,
                Category.type == type,
            )
        )
        return result.scalar_one_or_none()
