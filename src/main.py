from fastapi import FastAPI, HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from .routers import video, survey, picture, auth
from lib.get_today_class import get_today_classes
from lib.get_class_with_seat import get_class_with_seat
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database.operations import commit_sql
from lib.auth_operations import register_seat

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['http://localhost', 'http://localhost:5173'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]
app = FastAPI(middleware=middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/eventpoll/{type}')
async def event_poll(type: int):
    if type == 0:
        return get_class_with_seat()
    else:
        return get_today_classes()


class SeatInfo(BaseModel):
    student_id: str
    sn: int


@app.post('/seats')
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


class SurveyInfo(BaseModel):
    employee_id: str
    student_id: str
    rating: int
    dep_number: int


@app.post('/rate')
def rate_employee(survey_info: SurveyInfo):
    try:
        commit_sql(
            'rate_employee',
            student_id=survey_info.student_id,
            department=survey_info.dep_number,
            employee_id=survey_info.employee_id,
            rank=survey_info.rating
        )
    except Exception as e:
        print(e)
        raise HTTPException(404, '發生錯誤')


app.include_router(video.router)
app.include_router(survey.router)
app.include_router(picture.router)
app.include_router(auth.router)
