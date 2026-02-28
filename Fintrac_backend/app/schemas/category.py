from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class CategoryType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    DEBT = "debt"
    CREDIT = "credit"


class CategoryResponse(BaseModel):
    """Read-only response schema for predefined categories."""

    id: int
    name: str
    type: CategoryType
    color: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)
    parent_id: Optional[int] = None
    is_active: bool
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    class Config:
        from_attributes = True
