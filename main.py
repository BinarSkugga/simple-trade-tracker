import dataclasses
import os.path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from finance_api import get_stock_info

if not os.path.exists('frontend/dist'):
    os.mkdir('frontend/dist')

fastapi = FastAPI()


@fastapi.get('/stock/{symbol}')
async def stock_info(symbol: str):
    stock = get_stock_info(symbol)
    stock.monthly_return = stock.price * stock.dividend_yield / 12
    return stock

fastapi.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
