import logging
import uvicorn
from dotenv import load_dotenv

load_dotenv()

def runserver():
    from SyncUs import app
    return app


app = runserver()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=logging.INFO)