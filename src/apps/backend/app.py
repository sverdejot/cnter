from fastapi import FastAPI

from routers import counters

from Counter.infrastructure.odm.uMongoODM import instance

from bson.codec_options import CodecOptions
from bson.binary import STANDARD, JAVA_LEGACY, PYTHON_LEGACY, CSHARP_LEGACY

from dependencies import session_maker

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
    instance.set_db(session_maker.client.get_database('counter', CodecOptions(uuid_representation=STANDARD)))