from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from ..models.student_model import Student
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


class AuthData(BaseModel):
    student_id: str
    course: str

@router.post('/')
def check_student(auth_data: AuthData):
    try:
        student = Student(auth_data)
        return student
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)

