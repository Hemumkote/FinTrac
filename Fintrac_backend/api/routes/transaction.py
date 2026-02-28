from datetime import datetime
from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.common import APIResponse
from services.transaction_service import TransactionService
from app.db.session import get_async_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)


router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.post(
    "",
    status_code=201,
    summary="Create a new transaction",
    description="Create a new transaction for the authenticated user.",
)
async def create_transaction(
    transaction_data: TransactionCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[TransactionResponse]:
    service = TransactionService(session)
    transaction = await service.create_transaction(
        transaction_data, user_id=user.id
    )
    return APIResponse.created(
        data=transaction, message="transaction created successfully"
    )


@router.get(
    "/transactionByUser",
    status_code=200,
    summary="Get all transactions for a user",
    description="Retrieve all transactions for the authenticated user.",
)
async def get_transactions(
    type: str | None = None,
    category_id: list[int] | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    payment_method: str | None = None,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[Sequence[TransactionResponse]]:
    service = TransactionService(session)
    transactions = await service.get_transactions_by_user(
        user.id,
        type,
        category_id,
        from_date,
        to_date,
        payment_method,
        limit,
        offset,
    )
    return APIResponse.ok(
        data=transactions, message="Transaction fetched successfully", status=200
    )


@router.get(
    "/transactionDetails",
    status_code=200,
    summary="Get the transaction details",
    description="Retrive the details of a transaction based on User and transaction id",
)
async def get_transaction(
    trn_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[TransactionResponse]:
    service = TransactionService(session)
    transaction = await service.get_transaction_by_id(trn_id, user.id)
    return APIResponse.ok(
        data=transaction,
        message="Transaction details fetched successfully",
        status=200,
    )


@router.patch(
    "",
    status_code=200,
    summary="Update the transaction",
    description="Update the transaction based on the transaction id",
)
async def update_transaction(
    transaction: TransactionUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[TransactionResponse]:
    if user.id != transaction.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    service = TransactionService(session)
    updated_transaction = await service.update_transaction(transaction, user.id)
    return APIResponse.ok(
        data=updated_transaction,
        message="Transaction details updated successfully",
        status=200,
    )


@router.delete(
    "",
    status_code=200,
    summary=" Delete the transaction",
    description="Delete the transaction based on the id and user ID",
)
async def delete_transaction(
    txn_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[TransactionResponse]:
    service = TransactionService(session)
    deleted_transaction = await service.delete_transaction(txn_id, user.id)
    return APIResponse.ok(
        data=deleted_transaction,
        message="Transaction Deleted Successfully",
        status=200,
    )


@router.get(
    "/balance_summary",
    status_code=200,
    summary=" get balance summary the transaction",
    description="get balance summary the transaction based on the id and user ID",
)
async def get_balance_summary(
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> APIResponse[dict]:
    service = TransactionService(session)
    transaction_summary = await service.get_transaction_summary(
        user.id, start_date, end_date
    )
    return APIResponse.ok(
        data=transaction_summary, message="Summary fetched Successfully", status=200
    )
