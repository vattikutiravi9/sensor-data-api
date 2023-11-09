from fastapi import FastAPI
from routes import router as sensor_router
from database import Base, engine
from contextlib import asynccontextmanager
app = FastAPI()

app.include_router(sensor_router)


@asynccontextmanager
async def on_startup():
    Base.metadata.create_all(bind=engine)
