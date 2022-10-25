import secrets
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from passlib.hash import argon2
from starlette.requests import Request

from models.user import User
from repository import Repository

TOKEN_SECRET = secrets.token_bytes(32)


def hash_password(password: str):
    return argon2.using(rounds=6).hash(password)


def verify_password(password: str, hash: str):
    return argon2.verify(password, hash)


def decode_token(token: str) -> dict:
    decoded = jwt.decode(token, TOKEN_SECRET, algorithms=['HS256'])
    return decoded


def new_token(data: dict, expire: Optional[int]):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET, algorithm='HS256')
    return encoded_jwt


def auth(required_role: str):
    users = Repository('user', User)

    async def run(request: Request):
        try:
            token = request.headers.get('Authorization', None)
            if isinstance(token, str) and token.startswith('Bearer'):
                token = token.split('Bearer ')[1]

            # FIXME: Testing without login, remove this
            if token is None:
                token = new_token({'id': 1}, 0)
            decoded = decode_token(token)
            user = users.get(decoded['id'])

            if user.role != 'super_admin' and user.role != required_role:
                raise

            # Set the user's scope
            request.scope['user'] = user
            return user
        except Exception:
            raise HTTPException(401, 'not enough access')

    return Depends(run)
