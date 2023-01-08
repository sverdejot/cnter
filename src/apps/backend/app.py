from fastapi import FastAPI
from bson.codec_options import CodecOptions
from bson.binary import STANDARD

from Counter.infrastructure.odm.uMongoODM import instance

from routers import counters
from dependencies import motor_client
from config import settings


app = FastAPI(
    title='🔢 cnter',
    description='a counter-based social media app',
    version='0.1.0',
    contact={
        'name': 'Samuel Verdejo',
        'email': 'contacto@sverdejot.dev',
        'url': 'http://www.sverdejot.dev',
    }
)

app.include_router(counters.router)

@app.on_event('startup')
async def initialize_umongo_instance():
    instance.set_db(motor_client.get_database(settings.mongo_db_name, CodecOptions(uuid_representation=STANDARD)))
