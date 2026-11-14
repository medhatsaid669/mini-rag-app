from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
app = FastAPI() 

@app.get("/welcome")
def welcome():
    return {"message": "Welcome to the FastAPI application!"}
