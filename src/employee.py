from .database import execute_SQL
from datetime import datetime, timedelta


def dep_name_from_num(target_value):
    deps = {
        "招生部": 2,
        "櫃台": 4,
        "補課教室": 8,
        "數輔": 9,
        "導師組": 11
    }

    return next((k for k, v in deps.items() if v == target_value), None)


class Employee:
    def __init__(self, id):
        self.card_id = id
        self.picture = None

    @property
    def dep_number(self):
        return int(execute_SQL(
            'employee/department',
            'one',
            employee_id=self.card_id
        )[0])

    @staticmethod
    def working_today(voted_employees: list):
        # def GetTodayEmployeeDepartment(self):
        # def GetTodayEmployeesData(self):
        # def GetTodayEmployeeDepartment(self):
        #  def GetTodayTeacherData(self):

        res = execute_SQL(
            'all_employees',
            'all',
            current_date='2020-09-16'
        )

        return [
            {
                "id": t[0].strip(),
                "name": t[1].strip(),
                "department_number": t[2],
                "department_name": dep_name_from_num(t[2])
            } for t in res if t[0].strip() not in voted_employees
        ]
