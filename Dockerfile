FROM node:16-slim as builder

COPY . /app
WORKDIR /app

RUN cd frontend && npm install && npm run build


FROM python:3.8-slim as service

ARG port
ENV PORT=$port

COPY . /app
COPY --from=builder /app/frontend/dist /app/frontend/dist

WORKDIR /app

RUN pip install -U pip && pip install -r requirements.txt

CMD gunicorn -w 3 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT main:fastapi