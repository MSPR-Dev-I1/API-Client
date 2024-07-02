from fastapi import FastAPI
from app.routers import client, demo
from app.database import create_tables

app = FastAPI()


origins = ["*"]


app.include_router(client.router, prefix="/client")
app.include_router(demo.router, prefix="/demo")

@app.post("/create-database")
async def create_database():
    """
        Create database
    """
    create_tables()
    return "database created"
