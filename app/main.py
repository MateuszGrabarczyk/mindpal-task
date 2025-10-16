from fastapi import FastAPI
from app.api.items import router as items_router

app = FastAPI(title="Items API")

app.include_router(items_router)
