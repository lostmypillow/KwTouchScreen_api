from ..database import execute_SQL
from datetime import datetime, timedelta
from .employee_model import Employee
from fastapi import HTTPException




class Student:

    # sample_data = {
    #     "student_id": "300003",
    #     "auth_course": "試聽數學班",
    #     "name": "邱小傑1",
    #     "gender": "male",
    #     "rateable_employees": [
    #         {
    #             "id": "200952",
    #             "name": "朱彥妃",
    #             "department_number": 11,
    #             "department_name": "導師組"
    #         },
    #         {
    #             "id": "200979",
    #             "name": "唐翊倫",
    #             "department_number": 8,
    #             "department_name": "補課教室"
    #         },
    #         {
    #             "id": "201012",
    #             "name": "劉昭琪",
    #             "department_number": 2,
    #             "department_name": "招生部"
    #         },
    #         {
    #             "id": "201019",
    #             "name": "蔡東穎",
    #             "department_number": 11,
    #             "department_name": "導師組"
    #         },
    #         {
    #             "id": "201021",
    #             "name": "江佳儀",
    #             "department_number": 8,
    #             "department_name": "補課教室"
    #         },
    #         {
    #             "id": "200728",
    #             "name": "廖信瑜",
    #             "department_number": 11,
    #             "department_name": "導師組"
    #         },
    #         {
    #             "id": "200779",
    #             "name": "鄭羽雯",
    #             "department_number": 11,
    #             "department_name": "導師組"
    #         },
    #         {
    #             "id": "200805",
    #             "name": "鄭炳烽",
    #             "department_number": 8,
    #             "department_name": "補課教室"
    #         },
    #         {
    #             "id": "200864",
    #             "name": "游子頤",
    #             "department_number": 9,
    #             "department_name": "數輔"
    #         },
    #         {
    #             "id": "200935",
    #             "name": "張晏綺",
    #             "department_number": 11,
    #             "department_name": "導師組"
    #         }
    #     ],
    #     "voted_today": false
    # }

    def __init__(self, auth_data) -> None:
        self.student_id = auth_data.student_id
        self.auth_seat = False
        self.name = None
        self.gender = None
        self.rateable_employees = []
        self._check_existence()

    def _check_existence(self):
        # def getStudentName(self, id):
        try:
            details = execute_SQL(
                'student/details',
                'one',
                card_id=self.student_id
            )
            if details is None:
                raise HTTPException(status_code=404, detail="查無此人")

            self.student_id = details[0].strip()
            self.name = details[1].strip()

            if details[2] == '女':
                self.gender = 'female'
            elif details[2] == '男':
                self.gender = 'male'
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="發生錯誤")

    def check_match_class(self, number, name):
        data = execute_SQL(
                'student/get_classes',
                'all',
                student_id=self.student_id
            )
        check_select = execute_SQL('student/already_selected_today', 'all',
                                       class_id=number, student_id=self.student_id)
        if data[0][0] != name or check_select != []:
                raise HTTPException(status_code=404, detail="目前沒有您可選的補位資料")



    def check_rateable_employees(self):
        #  def GetVotedEmployeeByStudentIdWeekly(self, student_id):
        # today = datetime.now()
        today = datetime(2020, 9, 16).date()
        weekday = today.weekday()
        # monday = (today - timedelta(days=weekday)).strftime("%Y-%m-%d")
        monday = '2020-12-15 00:00:00.000'
        voted_employee_list = execute_SQL(
            'student/voted_employees',
            'all',
            monday=monday,
            student_id=self.student_id
        )

        employees_working_today = execute_SQL(
            'employee/working_today',
            'all',
            current_date='2020-09-16'
        )
        voted_employees = [x[0].strip() for x in voted_employee_list]
        self.rateable_employees = [
            {
                "id": data[0].strip(),
                "name": data[1].strip(),
                "department_number": data[2],
                "department_name": dep_name_from_num(data[2])
            } for data in employees_working_today if data[0].strip() not in voted_employees
        ]

    @staticmethod
    def register_seat(seat_data):
        # def add_class_seat_record(self, student_id, seat_id):
        try:
            execute_SQL(
                'student/register_seat',
                'commit',
                student_id=seat_data.student_id,
                sn=seat_data.sn
            )
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="發生錯誤")

    @staticmethod
    def rate(student_id, employee: Employee, rating):
        #  def addSatisfication(self, studentId, employeeId, rank):
        try:
            execute_SQL(
                'student/add_satisfaction',
                'commit',
                student_id=student_id,
                department=employee.dep_number,
                employee_id=employee.card_id,
                rank=rating
            )
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="發生錯誤")