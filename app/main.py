from fastapi import FastAPI
from app.api.api_router import api_router

app = FastAPI(title="Configuration Manager API")

app.include_router(api_router, prefix="/api")
