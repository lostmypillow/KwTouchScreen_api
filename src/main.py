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


class SeatInfo(BaseModel):
    student_id: str
    sn: int


class SurveyInfo(BaseModel):
    employee_id: str
    student_id: str
    rating: int
    dep_number: int


origins = ["*",]

app = FastAPI()
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


@app.get('/today_class')
async def stream_today_class():
    # return StreamingResponse()
    return get_today_classes()

@app.get('/class_with_seat')
async def stream_class_with_seat():
    return StreamingResponse(get_class_with_seat())

@app.post('/seat')
def register_seat(seat_info: SeatInfo):
    """_summary_

    Parameters
    ----------
    seat_info : SeatInfo
        _description_

    Raises
    ------
    HTTPException
        _description_
    """
    try:
        commit_sql(
            'student/register_seat',
            student_id=seat_info.student_id,
            sn=seat_info.sn
        )
    except Exception as e:
        print(e)
        raise HTTPException(404, '發生錯誤')


@app.post('/rate')
def rate_employee(survey_info: SurveyInfo):
    try:
        commit_sql(
            'rate_employee',
            student_id=survey_info.student_id,
            department=get_dep_number(survey_info.employee_id),
            employee_id=survey_info.employee_id,
            rank=survey_info.rating
        )
    except Exception as e:
        print(e)
        raise HTTPException(404, '發生錯誤')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        print(data)
        await websocket.send_text(f"Message text was: {data}")


app.include_router(video.router)
app.include_router(picture.router)
app.include_router(auth.router)
