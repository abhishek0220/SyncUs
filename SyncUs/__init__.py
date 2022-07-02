import pytz
from datetime import datetime
from fastapi import FastAPI

from SyncUs.utils.chat import socket_app


app = FastAPI(debug=True)

IST = pytz.timezone('Asia/Kolkata')
started_at = datetime.now(IST)


@app.get('/')
async def root():
    return {"project": "SyncUS", "status": "OK", "time_up": started_at}


app.mount("/", socket_app) 
