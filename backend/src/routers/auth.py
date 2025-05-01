from fastapi import APIRouter, HTTPException
from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from src.config import settings
from src.database.exec_sql import exec_sql
from src.lib.custom_logger import logger
from src.lib.get_class_with_seats import get_class_with_seats
from src.lib.deps import deps
from src.models.auth_request import AuthRequest
from src.models.auth_response import AuthResponse
from src.models.error_response import ErrorResponse
from src.models.rateable_employee import RateableEmployee
auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@auth_router.post('/',
                  summary="學生身份驗證",
                  description="根據學生 ID 與驗證種類進行身份驗證並回傳相關資訊",
                  response_model=AuthResponse,
                  responses={
                      200: {
                          "model": AuthResponse,
                          "description": "Student authorized successfully"
                      },
                      404: {
                          "model": ErrorResponse,
                          "description": "Not found - student, data, or rating target missing"
                      },
                  })
async def authorize_student(auth_request: AuthRequest):
    global settings
    try:
        student_details: dict[str, str] = await exec_sql(
            'one',
            'student_details',
            card_id=auth_request.student_id
        )
        print(student_details)
    # Example student_details value:
    # {
    #     "學號": "300003",
    #     "姓名": "邱小傑1",
    #     "性別": "男"
    # }
    except Exception as e:
        logger.exception(
            f'[AUTH {auth_request.student_id}] DB query student_details failed, raising Error 500')
        raise HTTPException(500, detail="抱歉，系統發生錯誤! Error 001")

    if student_details is None or student_details == {}:
        logger.error(
            f'[AUTH {auth_request.student_id}] No student found, raising Error 404')
        raise HTTPException(404, detail="抱歉，查無此人!")

    auth_response = AuthResponse(**student_details)

    if auth_request.type == 'awards':

        return auth_response

    if auth_request.type == "seat":

        try:
            class_with_seat = await get_class_with_seats()
        except Exception as e:
            logger.exception(
                f'[AUTH {auth_request.student_id}] Error calling get_class_with_seats(), raising Error 500')
            raise HTTPException(500, detail="抱歉，系統發生錯誤! Error 003")

        if class_with_seat == {}:
            raise HTTPException(404, "抱歉，目前沒有補位資料!")
        print(class_with_seat)

        try:
            courses_of_student: list[dict[str, str]] = await exec_sql(
                'all',
                'student_match_course',
                student_id=auth_request.student_id
            )
            print(courses_of_student)
        # Example courses_of_student value:
        # [
        #     {
        #         "班別": "試聽數學班"
        #     }
        # ]
        except Exception as e:
            logger.exception(
                f'[AUTH {auth_request.student_id}] DB query student_match_course failed, raising Error 500')
            raise HTTPException(500, detail="抱歉，系統發生錯誤! Error 002")

        if courses_of_student is None or courses_of_student == []:
            logger.error(
                f'[AUTH {auth_request.student_id}] No courses for {auth_request.student_id} found, raising Error 404')
            raise HTTPException(404, detail="抱歉，您沒有任何課程!")

        try:
            assert isinstance(courses_of_student, list)
            assert isinstance(class_with_seat, dict)

            matches_course = any(
                isinstance(
                    d, dict) and '班別' in d and d['班別'] == class_with_seat.get('班別')
                for d in courses_of_student
            )
        except AssertionError:
            logger.error(
                f"[AUTH {auth_request.student_id}] Data structure issue")
            raise HTTPException(500, "抱歉，系統發生錯誤! Error 004")

        except KeyError as e:
            logger.exception(
                f"[AUTH {auth_request.student_id}] Missing key: {e}")
            raise HTTPException(500, "抱歉，系統發生錯誤! Error 005")

        except Exception as e:
            logger.exception(
                f"[AUTH {auth_request.student_id}] Unknown error: {e}")
            raise HTTPException(500, "抱歉，系統發生錯誤! Error 006")

        if matches_course == False:
            logger.error(
                f'[AUTH {auth_request.student_id}] Student s courses does NOT match course for seat')
            raise HTTPException(404, detail="抱歉，目前沒有您可選的補位資料!")

        try:
            check_already_selected: list = await exec_sql(
                'all',
                'student_already_selected',
                course_id=class_with_seat['主檔號'],
                student_id=auth_request.student_id
            )
        except Exception as e:
            logger.exception(
                f'[AUTH {auth_request.student_id}] DB query student_already_selected failed, raising Error 500')
            raise HTTPException(500, detail="系統發生錯誤，error 007")
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

        if matches_course is False or check_already_selected != []:

            logger.error(f'[AUTH {auth_request.student_id}] 目前沒有您可選的補位資料')

            raise HTTPException(404, "目前沒有您可選的補位資料")

    elif auth_request.type == "survey":

        try:
            emp_working_today = await exec_sql(
                'all',
                'student_today_employees',
                current_date=datetime.now().strftime('%Y-%m-%d')
            )
        except Exception as e:
            logger.exception(
                f"[AUTH {auth_request.student_id}] Unknown error: {e}")
            raise HTTPException(500, "抱歉，系統發生錯誤! Error 008")

        if emp_working_today == []:
            raise HTTPException(404, "目前沒有可評分的員工")

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

        try:
            voted_emp_week = await exec_sql(
                'all',
                'student_voted_employees',
                monday=(datetime.now() - timedelta(days=datetime.now().weekday())
                        ).strftime('%Y-%m-%d 00:00:00.000'),
                student_id=auth_request.student_id
            )
        except Exception as e:
            logger.exception(
                f"[AUTH {auth_request.student_id}] Unknown error: {e}")
            raise HTTPException(500, "抱歉，系統發生錯誤! Error 009")

        rateable_employees = [
           RateableEmployee(**employee)
            for employee in emp_working_today
            if employee['學號'] not in [
                voted_emps['評分對象']
                for voted_emps in voted_emp_week
            ]
        ]

        if rateable_employees == []:

            raise HTTPException(404, "目前沒有可評分的員工")

        auth_response.rateable_employees = rateable_employees

    return auth_response
