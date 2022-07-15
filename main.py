import requests
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()


class BaseUrl(BaseModel):
    url: str


@app.get("/")
async def root():
    return {"message": "Keep alive server is working."}


@app.post("/alive/")
async def alive(url: BaseUrl, response: Response):
    response.status_code = callback(url.url)
    return response.status_code


def callback(url: str):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        return 400
    return response.status_code
