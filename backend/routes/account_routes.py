from fastapi import FastAPI

from auth_utils import auth
from config import WS_TFSA_ID
from interface.wealthsimple_api_interface import IWealthSimpleAPI


def load(fastapi: FastAPI, ws_api: IWealthSimpleAPI):

    @fastapi.get('/api/v1/account', dependencies=[auth('default')])
    def activities_list():
        return next((account for account in ws_api.accounts() if account.id == WS_TFSA_ID), None)
