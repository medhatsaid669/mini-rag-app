from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from routes import base, data
from routes import base, data  # pyright: ignore[reportMissingImports]  


app = FastAPI()

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(data.data_router, prefix="/data", tags=["Data Operations"])





