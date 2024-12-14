from fastapi import FastAPI, APIRouter, HTTPException
from ..student import Student
from ..database import execute_SQL
from pydantic import BaseModel
from ..course import Course

class SeatModel(BaseModel):
    student_id: str
    sn: int


router = APIRouter(
    prefix="/seats",
    tags=["Seats"],
)

@router.get('/remaining')
def get_class_with_seat():
    # def getSeatInfo(self):
    # def is_seat_system_available(self):
    return Course()

@router.get('/{student_id}')
def get_available_seats(student_id: str):
    try:
        student = Student(student_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    return student if student.name != None else HTTPException(status_code=404, detail="查無此人")


@router.post('/')
def register_seat(seat: SeatModel):
    student = Student(seat.student_id)
    print(student.name)
    try:
        student.register_seat(seat.sn)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="發生錯誤")
    return "選擇完成"
