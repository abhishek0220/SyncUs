import pytz
from datetime import datetime
from fastapi import FastAPI
from SyncUs.Schemas.auth import TokenSchema

from SyncUs.utils.chat import socket_app
from SyncUs.utils.spotify import spotifyWrapper


app = FastAPI(debug=True)

IST = pytz.timezone('Asia/Kolkata')
started_at = datetime.now(IST)


@app.get('/')
async def root():
    return {"project": "SyncUS", "status": "OK", "time_up": started_at}

@app.get("/oauth/url")
async def getAuthUrl():
    return {'url': spotifyWrapper.getOauthUrl()}

@app.get("/oauth/callback", response_model=TokenSchema)
async def getToken(code: str):
    return spotifyWrapper.getToken(code)

app.mount("/", socket_app) 
