from email import message
from typing import Annotated, Any, Generic, Optional, TypeVar
from pydantic import AfterValidator, BaseModel, Field


T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Individual error detail- used for validation of errors"""

    field: str = Field(description="Field that caused the error")
    message: str = Field(description="Error message")


class APIResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper
    every response returns in this shape
    """

    success: bool = Field(description="Indicates if the request was successful")
    status: int = Field(description="HTTP status code")
    message: str | None = Field(default=None, description="Response message")
    data: Optional[T] = Field(default=None, description="Response data")
    errors: Optional[list[ErrorDetail]] = Field(
        default=None, description="list of errors"
    )

    @classmethod
    def ok(cls, data: Any, message: str = "Success", status: int = 200):
        """shortcut foe successful responses"""
        return cls(success=True, status=status, message=message, data=data)

    @classmethod
    def created(
        cls, data: Any, message: str = "Created successfully", status: int = 201
    ):
        """Shortcut for 201 responses."""
        return cls(success=True, status=status, message=message, data=data)

    @classmethod
    def error(
        cls,
        message: str,
        status: int = 400,
        errors: Optional[list[ErrorDetail]] = None,
    ):
        """Shortcut for error responses."""
        return cls(
            success=False, status=status, message=message, data=None, errors=errors
        )


def name_field(
    min_length: int = 2,
    max_length: int = 50,
    description: str = "The name of the user",
    default: Any = ...,
) -> str:
    return Field(
        default=default,
        min_length=min_length,
        max_length=max_length,
        description=description,
    )


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
    if not any(char in special_characters for char in password):
        raise ValueError("Password must contain at least one special character")
    return password


StrongPassword = Annotated[str, AfterValidator(validate_password_strength)]
