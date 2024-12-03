from .student import Student
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger
from .seat import Seat
from fastapi.responses import FileResponse
from fastapi import FastAPI
from datetime import datetime
from .classroom import Classroom
from .database import Database
import base64


def get_classes_of_period(period: int):
    Classroom.get_scheduled(period, '2023/08/15')
    print(f"Task ran at {datetime.now()}!")


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


@app.get('/stu')
async def stu_name():
    # example_stu = Student(str(id))
    # result = Database.execute_SQL(
    #     'student_class', {"id": example_stu.student_id}, 'all')
    # print(result)

    # Classroom().get_scheduled(1, '2023/08/15')
    


    return 'ok'

@app.get('/employee/pic/{id}')
def get_employee_image(id: int):
    # def GetTodayEmployeePhotoByID(self, id):
    data = Database.execute_SQL('employee_image', {"id": id})
    print(type(data.照片))
    with open('image.png', 'wb') as file:
        file.write(data.照片)
    return FileResponse('image.png')
