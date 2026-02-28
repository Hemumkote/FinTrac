from datetime import datetime
from typing import Sequence
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)


class TransactionService:
    """
    Service class for transaction-related operations.
    """

    def __init__(self, session: AsyncSession):
        self.repository = TransactionRepository(session)
        self.session = session

    async def create_transaction(
        self, transaction_data: TransactionCreate, user_id: int
    ) -> TransactionResponse:
        """Create a new transaction."""
        category = await self.session.get(Category, transaction_data.category_id)
        if not category or category.type != transaction_data.type:
            raise HTTPException(status_code=404, detail="Category not matching")

        transaction = transaction_data.model_dump()
        transaction["user_id"] = user_id
        transaction = Transaction(**transaction)
        transaction = await self.repository.create_transaction(transaction)
        return TransactionResponse.model_validate(transaction)

    async def get_transactions_by_user(
        self,
        user_id: int,
        type: str | None = None,
        category_id: list[int] | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        payment_method: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[TransactionResponse]:
        transactions = await self.repository.get_transactions_by_user(
            user_id,
            type,
            category_id,
            from_date,
            to_date,
            payment_method,
            limit,
            offset,
        )
        return [TransactionResponse.model_validate(txn) for txn in transactions]

    async def get_transaction_by_id(
        self, transaction_id: int, user_id: int
    ) -> TransactionResponse:
        transaction = await self.repository.get_transaction_by_id(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        if transaction.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        return TransactionResponse.model_validate(transaction)

    async def update_transaction(
        self, transaction_data: TransactionUpdate, user_id: int
    ) -> TransactionResponse:
        """Update an existing transaction."""
        transaction = await self.repository.get_transaction_by_id(transaction_data.id)

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        for field, value in transaction_data.model_dump(
            exclude_unset=True, exclude={"id"}
        ).items():
            setattr(transaction, field, value)

        updated_transaction = await self.repository.update_transaction(transaction)

        return TransactionResponse.model_validate(updated_transaction)

    async def delete_transaction(
        self, transaction_id: int, user_id: int
    ) -> TransactionResponse:
        """Delete a transaction."""
        transaction = await self.repository.get_transaction_by_id(transaction_id)

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        if transaction.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        await self.repository.delete_transaction(transaction)

        return TransactionResponse.model_validate(transaction)

    async def get_transaction_summary(
        self, user_id: int, start_date: datetime, end_date: datetime
    ) -> dict[str, int]:
        """
        Get a summary of transactions for a user within a date range.

        Returns:
            dict: A dictionary containing summary information, e.g.:
                {
                    "total_income": float,
                    "total_expense": float,
                    "net_balance": float,
                    "category_breakdown": dict[str, float]
                }
        """

        summary = await self.repository.get_balance_summary(
            user_id, start_date, end_date
        )
        return summary
