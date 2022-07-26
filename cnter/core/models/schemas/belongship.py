from pydantic import (
    BaseModel,
)

from typing import List

from cnter.core.models.schemas import UserSchema
from cnter.core.models.schemas import CounterSchema

class BelongshipSchema(BaseModel):
    user: UserSchema
    counter: CounterSchema
    ts: List[float]
    joined: float