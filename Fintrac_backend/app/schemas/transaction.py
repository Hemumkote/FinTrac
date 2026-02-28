from dataclasses import field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models import user


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    DEBT = "debt"
    CREDIT = "credit"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    OTHER = "other"


class TransactionCreate(BaseModel):
    type: TransactionType = Field(
        description="Type of transaction: expense, income, debt, or credit",
    )
    user_id: int = Field(description="ID of the user associated with the transaction")
    category_id: int = Field(description="ID of the transaction category")
    amount: Decimal = Field(
        description="Amount of the transaction (must be > 0)",
        gt=0,
    )
    currency: str = Field(
        description="Currency code (e.g., 'INR', 'USD')",
        max_length=10,
        default="INR",
    )
    date: datetime = Field(description="Date and time of the transaction")
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional description of the transaction",
    )
    payee_payer: Optional[str] = Field(
        default=None, max_length=100, description="Name of the payee or payer"
    )
    payment_method: Optional[PaymentMethod] = Field(
        default=None, description="Payment method used for the transaction"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Additional notes about the transaction",
    )
    recept_url: Optional[str] = Field(
        default=None, max_length=255, description="URL of the transaction receipt"
    )
    is_recurring: Optional[bool] = Field(
        default=False, description="Indicates if the transaction is recurring"
    )

    @field_validator("type", mode="before")
    @classmethod
    def validate_amount(cls, V: TransactionType) -> TransactionType:
        allowed_types = {"expense", "income", "debt", "credit"}
        if V not in allowed_types:
            raise ValueError("Transaction type not allowed")
        return V

    @field_validator("currency", mode="before")
    @classmethod
    def validate_currency(cls, V: str) -> str:
        if not V or len(V) != 3:
            raise ValueError("Currency must be a 3-letter code (e.g., 'INR', 'USD')")
        return V.upper()

    @field_validator("date")
    @classmethod
    def validate_date(cls, V: datetime) -> datetime:
        if V > datetime.now():
            raise ValueError("Transaction date cannot be in the future")
        return V

    class Config:
        from_attributes = True

    # Response and Update schemas can reuse most of the fields from the Create schema, with some adjustments for optionality and additional metadata.


class TransactionResponse(BaseModel):
    id: int = Field(description="ID of the transaction")
    user_id: int = Field(description="ID of the user associated with the transaction")
    type: TransactionType = Field(
        description="Type of transaction: expense, income, debt, or credit",
    )
    category_id: int = Field(description="ID of the transaction category")
    amount: Decimal = Field(
        description="Amount of the transaction (must be > 0)",
        gt=0,
    )
    currency: str = Field(
        description="Currency code (e.g., 'INR', 'USD')",
        max_length=10,
        default="INR",
    )
    date: datetime = Field(description="Date and time of the transaction")
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional description of the transaction",
    )
    payee_payer: Optional[str] = Field(
        default=None, max_length=100, description="Name of the payee or payer"
    )
    payment_method: Optional[PaymentMethod] = Field(
        default=None, description="Payment method used for the transaction"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Additional notes about the transaction",
    )
    recept_url: Optional[str] = Field(
        default=None, max_length=255, description="URL of the transaction receipt"
    )
    is_recurring: bool = Field(
        default=False, description="Indicates if the transaction is recurring"
    )
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    id: int = Field(description="ID of the transaction to update")
    user_id: int = Field(description="ID of the user associated with the transaction")
    type: Optional[TransactionType] = Field(
        default=None,
        description="Type of transaction: expense, income, debt, or credit",
    )
    category_id: Optional[int] = Field(description="ID of the transaction category")
    amount: Optional[Decimal] = Field(
        default=None,
        description="Amount of the transaction (must be > 0)",
        gt=0,
    )
    currency: Optional[str] = Field(
        default=None,
        description="Currency code (e.g., 'INR', 'USD')",
        max_length=10,
    )
    date: Optional[datetime] = Field(description="Date and time of the transaction")
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional description of the transaction",
    )
    payee_payer: Optional[str] = Field(
        default=None, max_length=100, description="Name of the payee or payer"
    )
    payment_method: Optional[PaymentMethod] = Field(
        default=None, description="Payment method used for the transaction"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Additional notes about the transaction",
    )
    recept_url: Optional[str] = Field(
        default=None, max_length=255, description="URL of the transaction receipt"
    )
    is_recurring: Optional[bool] = Field(
        default=None, description="Indicates if the transaction is recurring"
    )

    class Config:
        from_attributes = True


class TransactionFilter(BaseModel):
    type: Optional[TransactionType] = Field(
        default=None,
        description="Filter by transaction type: expense, income, debt, or credit",
    )
    category_id: Optional[int] = Field(description="Filter by category ID")
    min_amount: Optional[Decimal] = Field(
        default=None,
        description="Filter transactions with amount greater than or equal to this value",
        gt=0,
    )
    max_amount: Optional[Decimal] = Field(
        default=None,
        description="Filter transactions with amount less than or equal to this value",
        gt=0,
    )
    start_date: Optional[datetime] = Field(
        default=None, description="Filter transactions on or after this date"
    )
    end_date: Optional[datetime] = Field(
        default=None, description="Filter transactions on or before this date"
    )
    payment_method: Optional[PaymentMethod] = Field(
        default=None, description="Filter transactions by payment method"
    )
