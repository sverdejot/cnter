from pydantic import BaseModel
from typing import Optional, ForwardRef
from datetime import datetime
from uuid import UUID

class Counter(BaseModel):
    id: UUID
    status: int = 0
    private: bool = False
    owner: ForwardRef('User')
    ts: Optional[datetime]

from cnter.core.models.schemas import User

Counter.update_forward_refs()