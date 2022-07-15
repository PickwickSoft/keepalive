import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseUrl(BaseModel):
    url: str


@app.get("/")
async def root():
    return {"message": "Keep alive server is working."}


@app.post("/alive/")
async def alive(url: BaseUrl):
    return callback(url.url)


def callback(url: str):
    return requests.get(url).status_code
