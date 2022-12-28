from fastapi import FastAPI

from backend.auth_utils import auth
from backend.interface.wealthsimple_api_interface import IWealthSimpleAPI
from backend.models.ws_position import WSPosition
from backend.repository import Repository


def load(fastapi: FastAPI, ws_api: IWealthSimpleAPI):
    positions = Repository('position', WSPosition)

    @fastapi.get('/api/v1/positions', dependencies=[auth('default')])
    def positions_get():
        return positions.list()

    @fastapi.get('/api/v1/positions/update', dependencies=[auth('default')])
    def positions_set():
        ws_positions = ws_api.positions()
        positions.truncate()
        for position in ws_positions:
            positions.upsert(position)

        return positions.list()
