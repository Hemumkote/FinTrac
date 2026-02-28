from datetime import datetime
from typing import List, Sequence
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(self, transaction: Transaction):
        """create a new transaction in the database."""
        self.session.add(transaction)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def get_transaction_by_id(self, transaction_id: int) -> Transaction | None:
        """Retrieve a transaction by its ID."""
        result = await self.session.get(Transaction, transaction_id)
        return result

    async def get_transactions_by_user(
        self,
        user_id: int,
        type: str | None = None,
        category_id: List[int] | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        payment_method: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Transaction]:
        """Retrieve all transactions for a specific user."""
        query = select(Transaction).where(Transaction.user_id == user_id)
        if type is not None:
            query = query.where(Transaction.type == type)
        if category_id is not None:
            query = query.where(Transaction.category_id.in_(category_id))
        if from_date is not None and to_date is not None:
            query = query.where(Transaction.date.between(from_date, to_date))
        if payment_method is not None:
            query = query.where(Transaction.payment_method == payment_method)
        query = query.order_by(Transaction.date.desc()).offset(offset).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_transaction(self, transaction: Transaction) -> Transaction:
        """Update a transaction in the database."""
        self.session.add(transaction)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def delete_transaction(self, transaction: Transaction) -> Transaction:
        """Delete a transaction from the database."""
        await self.session.delete(transaction)
        await self.session.flush()
        await self.session.commit()
        return transaction

    async def get_balance_summary(
        self, user_id: int, start_date: datetime, end_date: datetime
    ) -> dict:
        """Get the balance summary for a user within a date range."""
        result = await self.session.execute(
            select(
                func.sum(
                    case((Transaction.type == "income", Transaction.amount), else_=0)
                ).label("total_income"),
                func.sum(
                    case((Transaction.type == "expense", Transaction.amount), else_=0)
                ).label("total_expense"),
            ).where(
                Transaction.user_id == user_id,
                Transaction.date.between(start_date, end_date),
            )
        )
        total_income, total_expense = result.one()

        return {
            "total_income": total_income or 0,
            "total_expense": total_expense or 0,
            "balance": (total_income or 0) - (total_expense or 0),
        }
