from fastapi import FastAPI
from produce.celery import celery_app
from multiprocessing import Process
from dotenv import load_dotenv
import os

load_dotenv()

print(celery_app.tasks.keys())

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

