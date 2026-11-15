from fastapi import FastAPI  # pyright: ignore[reportMissingImports]

from dotenv import load_dotenv  # pyright: ignore[reportMissingImports] 
load_dotenv(".env")  # Load environment variables from .env file

#from routes.base import base_router  # pyright: ignore[reportMissingImports]

from routes import base 

app = FastAPI() 

app.include_router(base.base_router)


