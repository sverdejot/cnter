from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_endpoint_url: str
    mongo_username: str
    mongo_password: str
    mongo_port: int
    mongo_db_name: str

    class Config:
        env_file = '.env'

settings = Settings()
