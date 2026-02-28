from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.category import CategoryResponse, CategoryType
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    """Service layer for reading predefined categories."""

    def __init__(self, session: AsyncSession):
        self.repository = CategoryRepository(session)
        self.session = session

    async def get_categories(
        self, type: CategoryType | None = None
    ) -> list[CategoryResponse]:
        """Get all predefined categories, optionally filtered by type."""
        categories = await self.repository.get_all_categories(
            type=type.value if type else None
        )
        return [CategoryResponse.model_validate(category) for category in categories]

    async def get_category_by_id(self, category_id: int) -> CategoryResponse:
        """Get a single category by ID."""
        category = await self.repository.get_category_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return CategoryResponse.model_validate(category)
