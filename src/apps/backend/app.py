from fastapi import (
    FastAPI,
    status,
    Depends
)

from pydantic import (
    BaseModel,
    BaseSettings
)
from boto3 import Session
from uuid import UUID

from Counter.application.create import CounterCreator
from Counter.application.find import CounterFinder
from Counter.domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate,
)
from Counter.infrastructure.repositories.counter.DynamoDBCounterRepository import DynamoDBCounterRepository


class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    dynamodb_endpoint_url: str

    class Config:
        env_file = '.env'


settings = Settings()


class DynamoTable:
    def __init__(self, table_name: str):
        self.__table_name = table_name

    def __call__(self):
        session = Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )

        dyn = session.resource('dynamodb', endpoint_url=settings.dynamodb_endpoint_url)
        yield dyn.Table(self.__table_name)

class CounterRequestBody(BaseModel):
    ownerId: UUID
    private: bool

class CounterUpdateRequestBody(BaseModel):
    memberId: UUID
    ts: float

app = FastAPI()


counters_table = DynamoTable(table_name='counters')


@app.get('/counter/{counterId}', status_code=status.HTTP_200_OK)
async def get_counter(counterId: UUID, table = Depends(counters_table)):
    repo = DynamoDBCounterRepository(table)

    finder = CounterFinder(repo=repo)

    counter = finder(counterId=CounterId(counterId))

    return {
        'id': counter.counterId,
        'ownerId': counter.ownerId,
        'private': counter.private,
        'status': counter.status
    }


@app.post('/counter/{counterId}', status_code=status.HTTP_201_CREATED)
async def create_counter(counterId: UUID, counter: CounterRequestBody, table = Depends(counters_table)):
    repo = DynamoDBCounterRepository(table)

    creator = CounterCreator(repo)

    counterId = CounterId(counterId)
    ownerId = UserId(counter.ownerId)
    private = CounterPrivate(counter.private)

    creator(counterId=counterId, ownerId=ownerId, private=private)