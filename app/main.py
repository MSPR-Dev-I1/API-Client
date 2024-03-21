from fastapi import FastAPI
from routers import client

app = FastAPI()


origins = ["*"]


app.include_router(client.router, prefix="/client")
