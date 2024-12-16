from fastapi import FastAPI, APIRouter, HTTPException
from ..models.student_model import Student
from ..database import execute_SQL
from pydantic import BaseModel
from ..models.course_model import Course

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
    course = Course()
    return course if course.is_available else {}

# @router.get('/{student_id}')
# def get_available_seats(student_id: str):
#     try:
#         student = Student(student_id)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(e)
#     return student


@router.post('/')
def register_seat(seat_info: SeatModel):
    try:
        Student.register_seat(seat_info)
    except HTTPException as e:
        print(e)
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="發生錯誤")
    return Course()
