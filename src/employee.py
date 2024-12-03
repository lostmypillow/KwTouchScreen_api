from .database import execute_SQL
from datetime import datetime, timedelta

def working_today(self):
    # def GetTodayEmployeeDepartment(self):
    # def GetTodayEmployeesData(self):

    # print(execute_SQL('get_today_department', {}, 'all'))
    # def GetTodayEmployeeDepartment(self):
    # [('200900 ', '林禹馨', 8), ('200952 ', '朱彥妃', 11), ('200979 ', '唐翊倫', 8), ('200996 ', '梁嘉芸', 4), ('201012 ', '劉昭琪', 2), ('201019 ', '蔡東穎', 11), ('201021 ', '江佳儀', 8), ('200728 ', '廖信瑜', 11), ('200779 ', '鄭羽雯', 11), ('200805 ', '鄭炳烽', 8), ('200935 ', '張晏綺', 11)]
    specific_departments = {"2": "招生部",
                            "4": "櫃台", "8": "補課教室", "11": "導師組"}
    res = execute_SQL(
        'get_today_employees_data',
        'all',
        current_date='2020-09-16'
    )
    return [
        {
            "id": t[0],
            "name": t[1],
            "department": specific_departments[str(t[2])]
        } for t in res
    ]

def get_voted_emp_by_student(student_id):
    today = datetime.now()
    weekday = today.weekday()
    monday = (today - timedelta(days=weekday)).strftime("%Y-%m-%d")
    execute_SQL('get_voted_by_emp_by_student', 'all', monday=monday, student_id=student_id)