from .student import Student
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger
from .seat import Seat
from fastapi.responses import FileResponse
from fastapi import FastAPI
from datetime import datetime
from .database import execute_SQL
from .employee import get_voted_emp_by_student


def get_classes_of_period(period: int):
    result = execute_SQL(
            'scheduled_classes',
            'all',
            current_date=date, current_period=period
            )
    classroom_map = ["", "301教室", "302教室", "303教室", "305教室", "會議室"]
        # [(2, '微積分B班(13)共補', '09:00', 1), (3, '微積分C班共補(8)', '09:00', 1)]
    result_dict_list = [{"location": classroom_map[t[0]], "name": t[1], "time": t[2], "other": t[3] } for t in result]
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


@app.get('/stu')
async def stu_name():
    # example_stu = Student(str(id))
    # result = Database.execute_SQL(
    #     'student_class', {"id": example_stu.student_id}, 'all')
    # print(result)

    # Classroom().get_scheduled(1, '2023/08/15')
    print(get_voted_emp_by_student())

    


    return 'ok'

@app.get('/employee/pic/{id}')
def get_employee_image(id: int):
    # def GetTodayEmployeePhotoByID(self, id):
    data = Database.execute_SQL('employee_image', {"id": id})
    print(type(data.照片))
    with open('image.png', 'wb') as file:
        file.write(data.照片)
    return FileResponse('image.png')
