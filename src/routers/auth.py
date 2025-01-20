from fastapi import APIRouter,HTTPException
from typing import Any
from pydantic import BaseModel
from lib.auth_operations import check_existence, check_match, check_already_selected, check_rateable_employees

from database.async_operations import exec_sql

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

class AuthData(BaseModel):
    student_id: str
    course: Any
    type: str

@router.post('/')
async def check_student(auth_data: AuthData):
    """_summary_

    Parameters
    ----------
    auth_data : AuthData
        _description_

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    HTTPException
        _description_
    """

    try:
        student_details = await exec_sql(
            'one',
            'student_details',
            card_id=auth_data.student_id
            )
        if student_details and auth_data.type == "seats":
            
            matches_class = check_match(auth_data.course['other_name'])
            already_selected = check_already_selected(auth_data.course['main_number'], auth_data.student_id)
            if matches_class or already_selected:
                raise HTTPException(404, "目前沒有您可選的補位資料")
            else:
                return student_details
        elif student_details and auth_data.type == "survey":
            rateable_employees = check_rateable_employees()
            if not rateable_employees:
                raise HTTPException(404, "目前沒有可評分的員工")        
            else:
                student_details["rateable_employees"] = rateable_employees
                return student_details
                
        else:
            raise HTTPException(404, "查無此人")

    except Exception as e:
        print(e)
        raise HTTPException(404, "發生錯誤")



# @router.post('/')
# def check_student(auth_data: AuthData):
#     """_summary_

#     Parameters
#     ----------
#     auth_data : AuthData
#         _description_

#     Returns
#     -------
#     _type_
#         _description_

#     Raises
#     ------
#     HTTPException
#         _description_
#     """

#     try:
#         student_details = check_existence(auth_data.student_id)
#         if student_details and auth_data.type == "seats":
#             matches_class = check_match(auth_data.course['other_name'])
#             already_selected = check_already_selected(auth_data.course['main_number'], auth_data.student_id)
#             if matches_class or already_selected:
#                 raise HTTPException(404, "目前沒有您可選的補位資料")
#             else:
#                 return student_details
#         elif student_details and auth_data.type == "survey":
#             rateable_employees = check_rateable_employees()
#             if not rateable_employees:
#                 raise HTTPException(404, "目前沒有可評分的員工")        
#             else:
#                 student_details["rateable_employees"] = rateable_employees
#                 return student_details
                
#         else:
#             raise HTTPException(404, "查無此人")

#     except Exception as e:
#         print(e)
#         raise HTTPException(404, "發生錯誤")
    
