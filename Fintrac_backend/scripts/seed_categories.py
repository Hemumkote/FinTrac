"""
Seed script for predefined categories.

Run this script to populate the database with default categories.

Usage:
  From Fintrac_backend/:  python scripts/seed_categories.py
  From Docker container:  python scripts/seed_categories.py
"""

import asyncio
import os
import sys

# Ensure Fintrac_backend/ is on sys.path so 'app' and 'core' packages are importable.
# Works whether you run from Fintrac_backend/ or from scripts/ itself.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)  # Fintrac_backend/
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy import select  # noqa: E402

from app.db.session import get_async_context  # noqa: E402
from app.models.category import Category  # noqa: E402


DEFAULT_CATEGORIES = [
    # Expense Categories
    {"name": "Food & Dining", "type": "expense", "color": "#F97316", "icon": "food"},
    {"name": "Housing", "type": "expense", "color": "#7C3AED", "icon": "home"},
    {"name": "Transport", "type": "expense", "color": "#0EA5E9", "icon": "car"},
    {"name": "Shopping", "type": "expense", "color": "#EC4899", "icon": "shopping"},
    {"name": "Entertainment", "type": "expense", "color": "#8B5CF6", "icon": "gamepad"},
    {"name": "Utilities", "type": "expense", "color": "#06B6D4", "icon": "flash"},
    {"name": "Healthcare", "type": "expense", "color": "#EF4444", "icon": "heart-pulse"},
    {"name": "Education", "type": "expense", "color": "#F59E0B", "icon": "school"},
    {"name": "Subscriptions", "type": "expense", "color": "#6366F1", "icon": "refresh"},
    {"name": "Groceries", "type": "expense", "color": "#10B981", "icon": "cart"},
    {"name": "Personal Care", "type": "expense", "color": "#A855F7", "icon": "spa"},
    {"name": "Insurance", "type": "expense", "color": "#64748B", "icon": "shield"},
    {"name": "Gifts & Donations", "type": "expense", "color": "#F43F5E", "icon": "gift"},
    {"name": "Travel", "type": "expense", "color": "#0891B2", "icon": "airplane"},
    {"name": "Other Expense", "type": "expense", "color": "#6B7280", "icon": "dots-horizontal"},
    # Income Categories
    {"name": "Salary", "type": "income", "color": "#10B981", "icon": "cash"},
    {"name": "Freelance", "type": "income", "color": "#3B82F6", "icon": "briefcase"},
    {"name": "Investments", "type": "income", "color": "#6366F1", "icon": "trending-up"},
    {"name": "Business", "type": "income", "color": "#14B8A6", "icon": "store"},
    {"name": "Rental Income", "type": "income", "color": "#8B5CF6", "icon": "home-city"},
    {"name": "Gifts", "type": "income", "color": "#EC4899", "icon": "gift"},
    {"name": "Refunds", "type": "income", "color": "#F59E0B", "icon": "undo"},
    {"name": "Other Income", "type": "income", "color": "#6B7280", "icon": "dots-horizontal"},
]


async def seed_categories() -> None:
    """Insert default categories into the database if they don't already exist."""
    async with get_async_context() as session:
        inserted = 0
        skipped = 0

        for cat_data in DEFAULT_CATEGORIES:
            result = await session.execute(
                select(Category).where(
                    Category.name == cat_data["name"],
                    Category.type == cat_data["type"],
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                skipped += 1
                continue

            category = Category(
                name=cat_data["name"],
                type=cat_data["type"],
                color=cat_data["color"],
                icon=cat_data["icon"],
            )
            session.add(category)
            inserted += 1

        await session.flush()
        print(f"Seeding complete: {inserted} categories inserted, {skipped} already existed.")


if __name__ == "__main__":
    asyncio.run(seed_categories())
