from fastapi import FastAPI
from .routers import routes
from .database import init_mongodb, PostgresBase, engine
import asyncio

app = FastAPI(title="Tetor - Tech Interview AI Tutor",
              root_path = "/api")

@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        loop.run_in_executor(None, PostgresBase.metadata.create_all, engine),
        init_mongodb()
    )

for route in routes:
    app.include_router(route)

