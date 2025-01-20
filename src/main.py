from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from routers import video, picture, auth
from lib.get_today_class import get_today_classes
from lib.get_class_with_seat import get_class_with_seat
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database.operations import commit_sql, fetch_one_sql
from lib.get_dep_number import get_dep_number
from database.async_operations import async_engine, exec_sql
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
class SeatInfo(BaseModel):
    student_id: str
    sn: int


class SurveyInfo(BaseModel):
    employee_id: str
    student_id: str
    rating: int
    dep_number: int


origins = ["*",]

class KlasseResponse(BaseModel):
    """_summary_

    Attributes
    ----------
    classes_today : list[dict]
        _description_
    """
    classes_today: list[dict]
    """meow
    """
    klasse_with_seats: list
    # klasse is class in German, to avoid confusing it with class


async def send_updates() -> KlasseResponse:
    if 'client' in active_connections:
        await active_connections['client'].send_json(data)
    print("meow")

async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        send_updates,
        "interval",
        seconds=10

    )
    yield
    await async_engine.dispose()
    scheduler.shutdown()


app = FastAPI(


    lifespan=lifespan,

    # Here I define the title. This is purely cosmetic, and so you know which application's Swagger Doc you're looking at when you visit the "/docs" endpoint
    title="觸控螢幕 API / KwTouchScreen API",

    # Version is also arbitrary. I wasn't keeping track, and we (Gitea) don't have semantic versioning. I follow the ZeroVer convention by keeping the version number under (and never reaching) 1.0.0
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.get('/classes/{type}')
# async def event_poll(type: str):
#     classes_today = get_today_classes()
#     class_with_seat = get_class_with_seat()
#     if type == 0 and class_with_seat:
#         return class_with_seat
#     elif type == 1 and classes_today:
#         return classes_today
#     else:
#         raise HTTPException


# @app.get('/today_class')
# async def stream_today_class():
#     # return StreamingResponse()
#     return get_today_classes()

# @app.get('/class_with_seat')
# async def stream_class_with_seat():
#     return StreamingResponse(get_class_with_seat())

# @app.post('/seat')
# def register_seat(seat_info: SeatInfo):
#     """_summary_

#     Parameters
#     ----------
#     seat_info : SeatInfo
#         _description_

#     Raises
#     ------
#     HTTPException
#         _description_
#     """
#     try:
#         commit_sql(
#             'student/register_seat',
#             student_id=seat_info.student_id,
#             sn=seat_info.sn
#         )
#     except Exception as e:
#         print(e)
#         raise HTTPException(404, '發生錯誤')


# @app.post('/rate')
# def rate_employee(survey_info: SurveyInfo):
#     try:
#         commit_sql(
#             'rate_employee',
#             student_id=survey_info.student_id,
#             department=get_dep_number(survey_info.employee_id),
#             employee_id=survey_info.employee_id,
#             rank=survey_info.rating
#         )
#     except Exception as e:
#         print(e)
#         raise HTTPException(404, '發生錯誤')

# Store connected clients
active_connections: dict [str, WebSocket]= {}
@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await websocket.accept()
    active_connections[client_name] = websocket

    while True:
        data: dict = await websocket.receive_json()
        if "to" in data:
            recipient = data['to']
            if recipient in active_connections:
                await active_connections[recipient].send_json(data)
            

        # x= {
        #     "to": "control",
        #     "action": "request"
        # }
        # y = {
        #     "to": "client",
        #     "action": "send",
        #     "data": "meow"
        # }
        


# app.include_router(video.router)
# app.include_router(picture.router)
# app.include_router(auth.router)

@app.get('/testt')
async def welp() -> KlasseResponse:
    return KlasseResponse(classes_today=[], klasse_with_seats=[])

@app.get('/test')
async def test():
    x = await exec_sql('all', 'scheduled_classes',  current_date='2023/08/15', current_period=1)
    print(x)
    return x
