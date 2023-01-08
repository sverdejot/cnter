from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import ClientSession

from typing import AsyncGenerator

from config import settings


class MotorSessionMaker:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client

    async def __call__(self) -> AsyncGenerator[ClientSession, None]:
        async with await self.client.start_session() as session:
            yield session

def initialize_client(endpoint: str, username: str, password: str, port: int):
    return AsyncIOMotorClient(f"mongodb://{username}:{password}@{endpoint}", port)

motor_client = initialize_client(
    endpoint=settings.mongo_endpoint_url,
    username=settings.mongo_username,
    password=settings.mongo_password,
    port=settings.mongo_port
)

session_maker = MotorSessionMaker(motor_client)
