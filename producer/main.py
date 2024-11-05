from fastapi import FastAPI, BackgroundTasks
from stream.manager import streamManager
from stream.client import StreamMode
from obspy import UTCDateTime
import uvicorn
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

SOURCE_MSEED = "20090118_064750.mseed"


load_dotenv()
app = FastAPI()
PORT = os.getenv("PORT")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/playback")
# def playback(
#     background_task: BackgroundTasks,
#     start_time: str | None = None,
#     end_time: str | None = None,
# ):
#     if start_time is None:
#         # start_time = UTCDateTime("2023-10-22T20:00:00.00+07")
#         start_time = UTCDateTime("2019-12-31T18:18:28.00+07")
#     if end_time is None:
#         end_time = UTCDateTime(start_time) + 30 * 6
#     print(start_time)
#     print(end_time)
#     background_task.add_task(
#         streamManager.start, StreamMode.PLAYBACK, start_time, end_time
#     )
#     # streamManager.start(StreamMode.PLAYBACK, start_time, end_time)
#     return "ok"


@app.get("/live")
async def live(background_tasks: BackgroundTasks):
    print("Received request to start live streaming")
    background_tasks.add_task(lambda: streamManager.start(StreamMode.LIVE))
    return {"message": "Task triggered in the background"}

# @app.post("/idle")
# def idle(background_tasks: BackgroundTasks):
#     print("Received request to stop live streaming")
#     background_tasks.add_task(streamManager.start, StreamMode.IDLE)
#     return "ok"

# @app.get("/file")
# def file(background_tasks: BackgroundTasks, filename: str = SOURCE_MSEED):
#     print(f"Received request to stream from file: {filename}")
#     background_tasks.add_task(streamManager.start, StreamMode.FILE, filename)
#     return "ok"


if __name__ == "__main__":
    config = uvicorn.Config(
        "main:app", port=int(PORT), log_level="info", host="0.0.0.0"
    )
    server = uvicorn.Server(config)
    server.run()
    print('GASSS')
