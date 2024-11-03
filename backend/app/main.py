from fastapi import FastAPI
from .routers import routes
from .database import init_mongodb, PostgresBase, engine, SessionLocal
from app.scripts.populate_dummy_data import populate_dummy_data
import asyncio

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Tetor - Tech Interview AI Tutor",
              root_path = "/api")

# app.add_middleware(
#      CORSMiddleware, 
#      allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], 
#      allow_credentials=True,
# )

@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        loop.run_in_executor(None, PostgresBase.metadata.create_all, engine),
        init_mongodb()
    )
    with SessionLocal() as session:
        await populate_dummy_data(postgres_db=session)

for route in routes:
    app.include_router(route)

