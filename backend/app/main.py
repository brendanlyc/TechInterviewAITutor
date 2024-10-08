from fastapi import FastAPI
from .routers import routes

app = FastAPI(title="Tetor - Tech Interview AI Tutor",
              root_path = "/api")

for route in routes:
    app.include_router(route)

