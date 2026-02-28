from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint

from app.models.transaction import Transaction
from app.db.base import Base


class Category(Base):
    """Predefined system-level categories. Users cannot create or modify these."""

    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("name", "type", name="uq_category_name_type"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # 'income' or 'expense'
    color: Mapped[str] = mapped_column(String(7), nullable=True)
    icon: Mapped[str] = mapped_column(String(50), nullable=True)
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Relationships
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")
