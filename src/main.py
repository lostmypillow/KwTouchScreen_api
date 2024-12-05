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


@app.get('/seats/{student_id}', tags=["Seats"])
def get_available_seats(student_id: str):
    student = Student(student_id)
    if student.name == None:
        raise HTTPException(status_code=404, detail="查無此人")
    elif student.classes == None:
        raise HTTPException(status_code=404, detail="目前沒有您可選的補位資料,請洽總導師。")
    else:
        return {
            "id": student.student_id,
            "name": student.name,
            "gender": student.gender,
            "classes": student.classes
        }


@app.post('/seats/{student_id}/{sn}', tags=["Seats"])
def register_seat(student_id: str, sn: str):
    Student(student_id).register_seat(sn)
    # NO ERROR HANDLING HERE...YET?
    return "選擇完成"


@app.get('/survey/employees/{student_id}', tags=['Survey'])
def get_employees(student_id:str, departments: str):
    return Employee.working_today(
        '2020-09-16',
        'all',
        Student(student_id).voted_employees)


@app.get('/picture/{role}/{id}', tags=["Pictures"])
def get_employee_image(role:str, id: str):
    # def GetTodayEmployeePhotoByID(self, id):
    image_stream = BytesIO(execute_SQL(role+ '_image', "one", id=id).照片)
    image_stream.seek(0)
    return StreamingResponse(
        content=image_stream,
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=image.png"}
    )

