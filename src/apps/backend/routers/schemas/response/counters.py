from pydantic import BaseModel
from uuid import UUID

class CounterFindReponseBody(BaseModel):
    counterId: UUID
    ownerId: UUID
    private: bool
    status: int
    members: list[UUID]