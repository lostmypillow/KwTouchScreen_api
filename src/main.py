from .student import Student
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger
from .employee import Employee
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import FastAPI, HTTPException
from datetime import datetime
from .database import execute_SQL
from io import BytesIO
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class SurveyResult(BaseModel):
    employee_id: str
    student_id: str
    rating: int


class SeatModel(BaseModel):
    student_id: str
    sn: int


def get_classes_of_period(period: int):
    #   def getClassroomInfo(self):
    # date = datetime.now().strftime('%Y/%m/%d')
    date = '2023/08/15'
    result = execute_SQL(
        'scheduled_classes',
        'all',
        current_date=date, current_period=period
    )
    classroom_map = [
        "301教室",
        "302教室",
        "303教室",
        "305教室",
        "會議室"
    ]
    # [(2, '微積分B班(13)共補', '09:00', 1), (3, '微積分C班共補(8)', '09:00', 1)]
    result_dict_list = [
        {
            "location": classroom_map[t[0]-1], "name": t[1],
            "time": t[2],
            "other": t[3]
        } for t in result
    ]
    print(result_dict_list)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: get_classes_of_period(1),
                      CronTrigger(hour=0, minute=0))
    scheduler.add_job(lambda: get_classes_of_period(2),
                      CronTrigger(hour=12, minute=0))
    scheduler.add_job(lambda: get_classes_of_period(3),
                      CronTrigger(hour=18, minute=0))
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/seats/{student_id}', tags=["Seats"])
def get_available_seats(student_id: str):
    try:
        student = Student(student_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    return student if student.name != None else HTTPException(status_code=404, detail="查無此人")


@app.post('/seats', tags=["Seats"])
def register_seat(seat: SeatModel):
    student = Student(seat.student_id)
    print(student.name)
    try:
        student.register_seat(seat.sn)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return "選擇完成"


@app.get('/survey/employees/{student_id}', tags=['Survey'])
def get_employees(student_id: str):
    try:
        working_employees = Employee.working_today(
            Student(student_id).voted_employees)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return working_employees


@app.post('/survey', tags=['Survey'])
def send_survey(result: SurveyResult):
    try:
        Student(result.student_id).rate(
            Employee(result.employee_id), result.rating)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    return "填寫完成"


@app.get('/test')
def test():
    print(Student('300003').get_available_selection())
    return 'ok'


@app.get('/picture/{role}/{id}', tags=["Pictures"])
def get_employee_image(role: str, id: str):
    # def GetTodayEmployeePhotoByID(self, id):
    try:
        image_bytes = execute_SQL(role + '_image', "one", id=id).照片
        image_stream = BytesIO(image_bytes)
        image_stream.seek(0)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return StreamingResponse(
        content=image_stream,
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=image.png"}
    )
