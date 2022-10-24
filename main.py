from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

fastapi = FastAPI()
fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")


@fastapi.get('/test')
async def hello():
    return 'hello'
