from fastapi import FastAPI

from backend.auth_utils import auth
from backend.models.activity import Activity
from backend.repository import Repository
from interface.wealthsimple_api_interface import IWealthSimpleAPI


def load(fastapi: FastAPI, ws_api: IWealthSimpleAPI):
    activities = Repository('activity', Activity)

    @fastapi.get('/api/v1/activities', dependencies=[auth('default')])
    def activities_list():
        return activities.list()

    @fastapi.get('/api/v1/activities/update', dependencies=[auth('default')])
    def activities_set():
        ws_activities = ws_api.activities()
        activities.truncate()
        for activity in ws_activities:
            activities.upsert(activity)

        return activities.list()
