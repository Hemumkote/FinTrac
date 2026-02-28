from fastapi import APIRouter, Depends, Query
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user
from app.models.user import User
from app.db.session import get_async_session
from app.schemas.category import CategoryResponse, CategoryType
from app.schemas.common import APIResponse
from services.category_service import CategoryService


router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get(
    "",
    status_code=200,
    summary="Get all predefined categories",
    description="Retrieve all predefined categories, optionally filtered by type (income/expense).",
)
async def get_categories(
    type: Optional[CategoryType] = Query(
        default=None, description="Filter by category type: income or expense"
    ),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[list[CategoryResponse]]:
    service = CategoryService(session)
    categories = await service.get_categories(type=type)
    return APIResponse.ok(data=categories, message="Categories fetched successfully")


@router.get(
    "/{category_id}",
    status_code=200,
    summary="Get a category by ID",
    description="Retrieve a single predefined category by its ID.",
)
async def get_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[CategoryResponse]:
    service = CategoryService(session)
    category = await service.get_category_by_id(category_id)
    return APIResponse.ok(data=category, message="Category fetched successfully")
