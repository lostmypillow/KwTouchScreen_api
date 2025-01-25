from fastapi import APIRouter, HTTPException
from typing import Any, Literal
from pydantic import BaseModel
from app.lib.auth_operations import check_existence, check_match, check_already_selected, check_rateable_employees

from app.database.async_operations import exec_sql
from app.lib.custom_logger import logger
from app.lib.get_class_with_seats import get_class_with_seats
auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


class AuthData(BaseModel):
    """_summary_

    Attributes
    ----------
    student_id : str
        Student ID
    
    course: str
        班別
    
    course_num: int
        主檔號
    
    type: Literal['seats', 'survey']
        not to be confused with python types, either 'seats' or 'survey'
    """
    student_id: str
    type: Literal['seats', 'survey']


class AuthResponse(BaseModel):
    學號: str
    姓名: str
    性別: str
    rateable_employees: list = []


{
  "student_id": "300003",
  "course": "試聽數學班",
  "course_num": 4,
  "type": "survey"
}

@auth_router.post('/')
async def authorize_student(auth_data: AuthData) -> AuthResponse:
    """Authorize student and return appropriate data. See code at routers/auth.py

    Parameters
    ----------
    auth_data : AuthData
        See AuthData in Schemas section below

    Returns
    -------
    AuthResponse
        See AuthResponse in Responses section Code 200, or in Schemas section below.

    Raises
    ------
    HTTPException
        See router/auth.py for all HTTPException triggers.
    """
    logger.info(f'[AUTH {auth_data.student_id}] Processing auth data...')

    try:

        student_details: dict[str, str] = await exec_sql(
            'one',
            'student_details',
            card_id=auth_data.student_id
        )
        # OUTPUT:
        # {
        #     "學號": "300003",
        #     "姓名": "邱小傑1",
        #     "性別": "男"
        # }

        auth_response = AuthResponse(**student_details)

        if student_details and auth_data.type == "seats":

            logger.info(
                f'''[AUTH {auth_data.student_id}] Student details exist & auth is for seats''')

            courses_of_student: list[dict[str, str]] = await exec_sql(
                'all',
                'student_match_course',
                student_id=auth_data.student_id
            )
            # OUTPUT:
            # [
            #     {
            #         "班別": "試聽數學班"
            #     }
            # ]
            class_with_seat = await get_class_with_seats()

            matches_course: bool = any(
                d['班別'] == class_with_seat['班別']
                for d in courses_of_student
            )

            logger.info(
                f'''[AUTH {auth_data.student_id}] Student s course matches course for seats'''
                if matches_course else
                f'''[AUTH {auth_data.student_id}] Student s courses match course for seats'''
            )

            

            check_already_selected: list = await exec_sql(
                'all',
                'student_already_selected',
                course_id=class_with_seat['主檔號'],
                student_id=auth_data.student_id
            )
            # OUTPUT:
            # [
            #     {
            #         "sn": 55169,
            #         "主檔號": 4,
            #         "座位號": "A17",
            #         "學號": "300003",
            #         "登記時間": "2025-01-06T21:23:57.437000"
            #     }
            # ]

            # Technically, i should be doing the any() function like i did with match class.
            # But considering there's only one class for selection in a given day, and the SQL already checks for courses selected today, i just check if it's empty
            already_selected: bool = False if check_already_selected == [] else True

            logger.info(
                f'[AUTH {auth_data.student_id}] Student has already selected course'
                if already_selected else
                f'[AUTH {auth_data.student_id}] Student has not already selected course')

            if not matches_course or already_selected:

                logger.error(f'[AUTH {auth_data.student_id}] 目前沒有您可選的補位資料')

                raise HTTPException(404, "目前沒有您可選的補位資料")

            else:

                logger.info(
                    f'[AUTH {auth_data.student_id}] Success! Returned data!')

                return auth_response

        elif student_details and auth_data.type == "survey":

            logger.info(
                f'[AUTH {auth_data.student_id}] Student details exist and auth is for survey')

            deps = {
                "招生部": 2,
                "櫃台": 4,
                "補課教室": 8,
                "數輔": 9,
                "導師組": 11
            }

            emp_working_today = await exec_sql(
                'all',
                'student_today_employees',
                current_date='2020-09-16'
            )

            for employee in emp_working_today:

                if "學號" in employee:

                    employee['學號'] = employee['學號'].strip()

                if '主要部門' in employee:

                    employee['主要部門'] = next((
                        k
                        for k, v in deps.items()
                        if v == employee['主要部門']),
                        None
                    )

            voted_emp_week = await exec_sql(
                'all',
                'student_voted_employees',
                monday='2020-12-15 00:00:00.000',
                student_id='300003'
            )

            rateable_employees = [
                y
                for y in emp_working_today
                if y['學號'] not in [
                    x['評分對象']
                    for x in voted_emp_week
                ]
            ]

            if rateable_employees == []:

                logger.error(f'[AUTH {auth_data.student_id}] 目前沒有可評分的員工')

                raise HTTPException(404, "目前沒有可評分的員工")
            
            else:

                auth_response.rateable_employees = rateable_employees

                logger.info(f'[AUTH {auth_data.student_id}] Success! Returned data!')

                return auth_response

        else:

            logger.error(f'[AUTH {auth_data.student_id}] 查無此人')

            raise HTTPException(404, "查無此人")

    except Exception as e:

        logger.error(f'[AUTH {auth_data.student_id}] {e}')

        raise HTTPException(404, "發生錯誤")
# {
#   "學號": "300003",
#   "姓名": "邱小傑1",
#   "性別": "男",
#   "rateable_employees": [
#     {
#       "學號": "200023",
#       "姓名": "戴佑安",
#       "主要部門": "數輔"
#     },
#     {
#       "學號": "200900",
#       "姓名": "林禹馨",
#       "主要部門": "補課教室"
#     },
#     {
#       "學號": "200952",
#       "姓名": "朱彥妃",
#       "主要部門": "導師組"
#     },
#     {
#       "學號": "200979",
#       "姓名": "唐翊倫",
#       "主要部門": "補課教室"
#     },
#     {
#       "學號": "200996",
#       "姓名": "梁嘉芸",
#       "主要部門": "櫃台"
#     },
#     {
#       "學號": "201012",
#       "姓名": "劉昭琪",
#       "主要部門": "招生部"
#     },
#     {
#       "學號": "201019",
#       "姓名": "蔡東穎",
#       "主要部門": "導師組"
#     },
#     {
#       "學號": "200728",
#       "姓名": "廖信瑜",
#       "主要部門": "導師組"
#     },
#     {
#       "學號": "200779",
#       "姓名": "鄭羽雯",
#       "主要部門": "導師組"
#     },
#     {
#       "學號": "200805",
#       "姓名": "鄭炳烽",
#       "主要部門": "補課教室"
#     },
#     {
#       "學號": "200864",
#       "姓名": "游子頤",
#       "主要部門": "數輔"
#     },
#     {
#       "學號": "200935",
#       "姓名": "張晏綺",
#       "主要部門": "導師組"
#     }
#   ]
# }