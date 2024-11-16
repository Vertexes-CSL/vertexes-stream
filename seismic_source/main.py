from fastapi import FastAPI, BackgroundTasks
from produce.manager import streamManager
from produce.client import StreamMode
from obspy import UTCDateTime
import uvicorn
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
app = FastAPI()
PORT = os.getenv("PORT")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/start")
async def live(background_tasks: BackgroundTasks):
    print("Received request to start live streaming")
    background_tasks.add_task(streamManager.start, StreamMode.LIVE)
    return {"message": "Task triggered in the background"}

@app.post("/idle")
def idle(background_tasks: BackgroundTasks):
    print("Received request to stop live streaming")
    background_tasks.add_task(streamManager.stop, StreamMode.IDLE)
    return "ok"


if __name__ == "__main__":
    config = uvicorn.Config(
        "main:app", port=int(PORT), log_level="info", host="0.0.0.0"
    )
    server = uvicorn.Server(config)
    server.run()
