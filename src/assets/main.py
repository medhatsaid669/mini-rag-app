from http import client

from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from routes import base, data  # pyright: ignore[reportMissingImports]  
from motor.motor_asyncio import AsyncIOMotorClient  # pyright: ignore[reportMissingImports] 
from helpers.config import get_settings  # pyright: ignore[reportMissingImports]    



app = FastAPI()

# Initialize the database connection
settings = get_settings()
client = AsyncIOMotorClient(settings.MongoDB_URI)
db = client[settings.MongoDB_NAME]

# Startup event to initialize the database connection
@app.on_event("startup")  
async def startup_event():
    app.state.db = db

# Shout down the database connection when the application stops
@app.on_event("shutdown")
async def shutdown_event():
    client.close()

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(data.data_router, prefix="/data", tags=["Data Operations"])





