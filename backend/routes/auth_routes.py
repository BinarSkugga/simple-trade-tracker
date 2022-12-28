from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from backend.auth_utils import verify_password, new_token, auth
from backend.models.user import User
from backend.payloads.login import Login
from backend.repository import Repository


def load(fastapi: FastAPI):
    users = Repository('user', User)

    @fastapi.post('/api/v1/login')
    def login(payload: Login):
        user: User = next(users.find('username', payload.username), None)
        if user is None:
            raise HTTPException(401, 'bad login')
        if not verify_password(payload.password, user.password_hash):
            raise HTTPException(401, 'bad login')

        return {'access_token': new_token({'id': user.id}, 0)}

    @fastapi.get('/api/v1/me', dependencies=[auth('default')])
    def me(request: Request):
        return request.scope['user']
