from fastapi import FastAPI

from auth_utils import auth
from interface.wealthsimple_api_interface import IWealthSimpleAPI
from models.stock import Stock
from repository import Repository


def load(fastapi: FastAPI, ws_api: IWealthSimpleAPI):
    stocks = Repository('stock', Stock)

    @fastapi.get('/api/v1/watchlist', dependencies=[auth('default')])
    def watchlist_get():
        return stocks.list()

    @fastapi.get('/api/v1/watchlist/update', dependencies=[auth('default')])
    def watchlist_set():
        watchlist_stocks = ws_api.watchlist()
        stocks.truncate()
        for w_stock in watchlist_stocks:
            stocks.upsert(w_stock)

        return stocks.list()
