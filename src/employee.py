from .database import execute_SQL
from datetime import datetime, timedelta




class Employee:
    def __init__(self, id):
        self.card_id = id
        self.picture = None

    @property
    def department(self):
        return execute_SQL(
            'get_department',
            'one',
            employee_id=self.card_id
        )

    @staticmethod
    def working_today(current_date: str, departments: str, excluded_employees: list):
        # def GetTodayEmployeeDepartment(self):
        # def GetTodayEmployeesData(self):
        # def GetTodayEmployeeDepartment(self):
        #  def GetTodayTeacherData(self):

        # [('200900 ', '林禹馨', 8), ('200952 ', '朱彥妃', 11), ('200979 ', '唐翊倫', 8), ('200996 ', '梁嘉芸', 4), ('201012 ', '劉昭琪', 2), ('201019 ', '蔡東穎', 11), ('201021 ', '江佳儀', 8), ('200728 ', '廖信瑜', 11), ('200779 ', '鄭羽雯', 11), ('200805 ', '鄭炳烽', 8), ('200935 ', '張晏綺', 11)]
        deps = {
            "招生部": 2,
            "櫃台": 4,
            "補課教室": 8,
            "數輔": 9,
            "導師組": 11
        }
        sql_file = 'all_employees' if departments == 'all' else 'math_employees'

        res = execute_SQL(
            sql_file,
            'all',
            current_date=current_date
        )

        return [
            {
                "id": t[0].strip(),
                "name": t[1].strip(),
                "department": list(deps.keys())
                [list(deps.values()).index(t[2])]
            } for t in res if t[0].strip() not in excluded_employees
        ]

