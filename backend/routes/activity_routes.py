from fastapi import FastAPI

from backend.auth_utils import auth
from backend.models.activity import Activity
from backend.repository import Repository


def load(fastapi: FastAPI):
    activities = Repository('activity', Activity)

    @fastapi.get('/api/v1/activities', dependencies=[auth('default')])
    def activities_list():
        return activities.list()
