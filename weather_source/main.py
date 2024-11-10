# from fastapi import FastAPI, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from produce.manager import scheduled_fetch_and_send
# from dotenv import load_dotenv
# import os

# load_dotenv()
# app = FastAPI()
# PORT = os.getenv("PORT")

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def read_root():
#     return {"message": "Weather service running"}

# @app.get("/start")
# def start_task():
#     scheduled_fetch_and_send.apply_async(countdown=10)
#     return {"message": "Weather data collection started"}

from fastapi import FastAPI
from produce.celery import celery_app
from multiprocessing import Process
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

def start_celery():
    worker = Process(target=celery_app.worker_main, args=(["worker", "--beat", "--scheduler", "celery.beat.PersistentScheduler"],))
    worker.start()

@app.on_event("startup")
def startup_event():
    start_celery()

@app.get("/")
def read_root():
    return {"message": "Weather service running"}

