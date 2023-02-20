from fastapi import FastAPI

from auth_utils import auth
from models.activity import Activity
from repository import Repository


def load(fastapi: FastAPI):
    activities = Repository('activity', Activity)

    @fastapi.get('/api/v1/activities', dependencies=[auth('default')])
    def activities_list():
        return activities.list()
