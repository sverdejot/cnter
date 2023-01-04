from fastapi import (
    FastAPI,
    status,
    Depends
)

from pydantic import (
    BaseModel,
    BaseSettings
)

from uuid import UUID

from Counter.application.create import CounterCreator
from Counter.application.find import CounterFinder
from Counter.application.join import CounterJoiner
from Counter.application.increment import CounterIncrementer

from Counter.infrastructure.repositories.counter.MotorCounterRepository import MotorCounterRepository

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import ClientSession

from Counter.domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate,
)


class Settings(BaseSettings):
    mongo_endpoint_url: str
    mongo_username: str
    mongo_password: str
    mongo_port: int

    class Config:
        env_file = '.env'

settings = Settings()

class MotorConnection:
    def __init__(self, endpoint: str, username: str, password: str, port: int):
        self.client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{endpoint}", port)

    async def __call__(self):
        async with await self.client.start_session() as session:
            yield session


class CounterCreateRequestBody(BaseModel):
    ownerId: UUID
    private: bool

class CounterUpdateRequestBody(BaseModel):
    memberId: UUID
    ts: float

class CounterJoinRequestBody(BaseModel):
    userId: UUID

class CounterFindReponseBody(BaseModel):
    counterId: UUID
    ownerId: UUID
    private: bool
    status: int
    members: set[UUID]

class CounterIncrementRequestBody(BaseModel):
    userId: UUID
    ts: float


session_maker = MotorConnection(
    endpoint=settings.mongo_endpoint_url,
    username=settings.mongo_username,
    password=settings.mongo_password,
    port=settings.mongo_port
)

app = FastAPI()


@app.get('/counter/{counterId}', status_code=status.HTTP_200_OK)
async def get_counter(counterId: UUID, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)

    finder = CounterFinder(repo=repo)

    counter = await finder(CounterId(counterId))

    return {
        'counterId': str(counter.counterId),
        'status': counter.status
    }

@app.post('/counter/{counterId}', status_code=status.HTTP_201_CREATED)
async def create_counter(counterId: UUID, counter: CounterCreateRequestBody, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)

    creator = CounterCreator(repo)

    await creator(counterId=CounterId(counterId), ownerId=UserId(counter.ownerId), private=CounterPrivate(counter.private))

@app.put('/counter/join/{counterId}', status_code=status.HTTP_201_CREATED)
async def join_counter(counterId: UUID, member: CounterJoinRequestBody, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)

    joiner = CounterJoiner(repo)

    await joiner(CounterId(counterId), UserId(member.userId))

@app.put('/counter/increment/{counterId}')
async def increment_counter(counterId: UUID, increment: CounterIncrementRequestBody, session: ClientSession = Depends(session_maker)):
    repo = MotorCounterRepository(session)

    incrementer = CounterIncrementer(repo)

    await incrementer(CounterId(counterId), UserId(increment.userId))
