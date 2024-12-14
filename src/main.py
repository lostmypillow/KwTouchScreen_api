from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
import time
from fastapi.middleware.cors import CORSMiddleware
from .routers import video, seats, survey, classes, picture
from typing import Optional
active_websocket: Optional[WebSocket] = None

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(lambda: get_classes_of_period(1),
#                       CronTrigger(hour=0, minute=0))
#     scheduler.add_job(lambda: get_classes_of_period(2),
#                       CronTrigger(hour=12, minute=0))
#     scheduler.add_job(lambda: get_classes_of_period(3),
#                       CronTrigger(hour=18, minute=0))
#     scheduler.start()
#     yield

# app = FastAPI(lifespan=lifespan)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print("Request took {} sec".format(time.time() - start_time))
    return response


app.include_router(video.router)
app.include_router(seats.router)
app.include_router(survey.router)
app.include_router(classes.router)
app.include_router(picture.router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global active_websocket
    await websocket.accept()
    active_websocket = websocket
    print("client connected")
    await websocket.send_json(
        {
            "device": "device.id",
            "image": "teacher.id",
            "teacher": "teacher.name",
            "school": "teacher.school"
        }
    )
    try:
        while True:
            message = await websocket.receive_text()
    except WebSocketDisconnect:
        active_websocket = None
        print("Client disconnected")
