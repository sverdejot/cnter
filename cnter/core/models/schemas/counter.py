from pydantic import BaseModel
from typing import Optional, ForwardRef
from datetime import datetime
from uuid import UUID

class CounterSchema(BaseModel):
    id: Optional[UUID]
    status: int = 0
    private: bool = False
    owner: ForwardRef('UserSchema')
    ts: Optional[datetime]

from cnter.core.models.schemas import UserSchema

CounterSchema.update_forward_refs()