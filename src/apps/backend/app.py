from fastapi import FastAPI

from routers import counters

app = FastAPI(
    title='🔢 cnter',
    description='a counter-based social media app',
    version='0.1.0',
    contact={
        'name': 'Samuel Verdejo',
        'email': 'contacto@sverdejot.dev',
        'url': 'www.sverdejot.dev',
    }
)

app.include_router(counters.router)