

from typing import Annotated
from pydantic import AfterValidator, Field





def name_field(
        min_length: int = 2, max_length: int = 50,description: str = "The name of the user"
)->str:
    return Field(
        min_length=min_length,
        max_length=max_length,
        description=description
    )
    
def validate_password_strength(password: str) -> str:
    if(len(password)<8):
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