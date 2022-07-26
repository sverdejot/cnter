from pydantic import (
    BaseModel, 
    Field,
    SecretStr,
    ValidationError,
    validator,
)

from uuid import UUID
from typing import List, Optional
from uuid import uuid4
from re import compile, match

PSSWD_CONST_RGX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'

class UserSchema(BaseModel):
    id: Optional[UUID]
    username: str = ...
    password: SecretStr = Field(..., min_length=8)

    @validator('password')
    def special_chars_psswd(cls, psswd):
        if not match(PSSWD_CONST_RGX, psswd.get_secret_value()):
            raise ValidationError(
                'psswd must contain at least one number, one lower-case letter and one capital-case letter'
            )
        return psswd