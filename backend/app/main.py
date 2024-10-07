from fastapi import FastAPI
from .routers import user

app = FastAPI(title="Tetor - Tech Interview AI Tutor",
              root_path = "/api")

app.include_router(user.router)

