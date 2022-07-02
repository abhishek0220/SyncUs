import pytz
import uuid
from loguru import logger
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import iterate_in_threadpool
from SyncUs.Schemas.auth import TokenSchema
from starlette.routing import Match

from SyncUs.utils.chat import socket_app
from SyncUs.utils.spotify import spotifyWrapper

IST = pytz.timezone('Asia/Kolkata')
started_at = datetime.now(IST)

fileName = f"logs/{started_at.strftime('%Y-%m-%d_%H-%M-%S')}_{''.join(str(uuid.uuid4()).split('-'))}.log"
logger.add(fileName, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | <level>{message}</level>")

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*')

@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} | {request.client.host}:{request.client.port} | {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
                logger.debug(f"{scope['path_params'].items()}")

    logger.debug(f"Headers: {request.headers.items()}")

    response = await call_next(request)
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    print(f"response_body={response_body}")

    logger.debug(f"Response: {b''.join(response_body).decode()}")
    return response


@app.get('/')
async def root():
    return {"project": "SyncUS", "status": "OK", "time_up": started_at}

@app.get("/oauth/url")
async def getAuthUrl():
    return {'url': spotifyWrapper.getOauthUrl()}

@app.get("/oauth/callback", response_model=TokenSchema)
async def getToken(code: str):
    token = spotifyWrapper.getToken(code)
    return token

app.mount("/", socket_app) 
