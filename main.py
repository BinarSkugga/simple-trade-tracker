from fastapi import FastAPI

fastapi = FastAPI()


@fastapi.get('/test')
async def hello():
    return 'hello'
