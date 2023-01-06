from pydantic import BaseModel
from uuid import UUID

class CounterCreateRequestBody(BaseModel):
    ownerId: UUID
    private: bool

class CounterJoinRequestBody(BaseModel):
    userId: UUID

class CounterIncrementRequestBody(BaseModel):
    userId: UUID
    ts: float

class CounterLeaveRequestBody(BaseModel):
    memberId: UUID
    ownerId: UUID | None