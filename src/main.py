from .student import Student
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger
from .employee import Employee
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from datetime import datetime
from .database import execute_SQL
from .employee import get_voted_emp_by_student


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


@app.get('/seat/{card_id}')
async def stu_name(card_id: int):
    student = Student(card_id)
    if student.name == None:
        raise HTTPException(status_code=404, detail="查無此人")
    elif student.classes == None:
        raise HTTPException(status_code=404, detail="目前沒有您可選的補位資料,請洽總導師。")

    # example_stu = Student(str(id))
    # result = Database.execute_SQL(
    #     'student_class', {"id": example_stu.student_id}, 'all')
    # print(result)

    # Classroom().get_scheduled(1, '2023/08/15')


@app.get('/survey')
return 'ok'


@app.get('/employee/pic/{id}')
def get_employee_image(id: int):
    # def GetTodayEmployeePhotoByID(self, id):
    data = Database.execute_SQL('employee_image', {"id": id})
    print(type(data.照片))
    with open('image.png', 'wb') as file:
        file.write(data.照片)
    return FileResponse('image.png')
