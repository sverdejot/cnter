from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import ClientSession

from typing import AsyncGenerator

from config import settings

class MotorConnection:
    def __init__(self, endpoint: str, username: str, password: str, port: int):
        self.client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{endpoint}", port)

    async def __call__(self) -> AsyncGenerator[ClientSession, None]:
        async with await self.client.start_session() as session:
            yield session


session_maker = MotorConnection(
    endpoint=settings.mongo_endpoint_url,
    username=settings.mongo_username,
    password=settings.mongo_password,
    port=settings.mongo_port
)