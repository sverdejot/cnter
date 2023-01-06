from fastapi import FastAPI

from routers import counters

app = FastAPI()

app.include_router(counters.router)