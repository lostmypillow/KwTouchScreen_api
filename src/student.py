from .database import execute_SQL
from datetime import datetime, timedelta
from .employee import Employee
from fastapi import HTTPException

def is_system_available():
    # def is_seat_system_available(self):
    return True if execute_SQL('seat_system_availability') else False


def get_remaining_seats():
    # def getSeatInfo(self):
    results = execute_SQL('remaining_seats', 'all')
    results_dict = [
        {
            'name': t[0],
            'male': t[1],
            'female': t[2]
        } for t in results
    ]
    print(results_dict)


class Student:

    def __init__(self, student_id) -> None:
        self.student_id = student_id
        self.name = None
        self.gender = None
        self.classes = None
        self._get_name_and_gender()
        self._get_classes()

    def _get_name_and_gender(self):
        # def getStudentName(self, id):
        details = execute_SQL(
            'student_details',
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

    def _get_classes(self):
        # def getClasses(self, id):
        result = []
        if self.student_id is not None:

            data = execute_SQL(
                'get_classes',
                'all',
                student_id=self.student_id
            )
            for item in data:

                already_selected_today = True if execute_SQL('already_selected_today',
                                                             'one',
                                                             student_id=self.student_id,
                                                             class_id=item[3]
                                                             ) else False
                sql_file = 'student_seats_male' if self.gender == 'male' else 'student_seats_female'
                available_seats = execute_SQL(sql_file,
                                              'all',
                                              class_id=item[3])

                if not already_selected_today and available_seats is not None:
                    result = [{
                        "name": item[0],
                        "sn": item[1],
                        "班別代碼": int(item[2].strip()),
                        "班級代碼": item[3],
                        "start_date": item[4].strftime('%Y-%m-%d %H:%M:%S'),
                        "who_set_it": item[5],
                        "starts_on": item[6].strftime('%Y-%m-%d %H:%M:%S'),
                        "ends_on": item[7].strftime('%Y-%m-%d %H:%M:%S'),
                        "set_on": item[8].strftime('%Y-%m-%d %H:%M:%S'),
                        "seats": [
                            {
                                "sn": seat[0],
                                "主檔號": seat[1],
                                "座位號": seat[2]
                            } for seat in available_seats
                        ]
                    } for item in data]

        self.classes = result

    def register_seat(self, sn):
        # def add_class_seat_record(self, student_id, seat_id):
        execute_SQL('register_seat',
                    'commit',
                    student_id=self.student_id,
                    sn=sn
                    )

    @property
    def voted_employees(self):
        #  def GetVotedEmployeeByStudentIdWeekly(self, student_id):
        # today = datetime.now()
        today = datetime(2020, 9, 16).date()
        weekday = today.weekday()
        # monday = (today - timedelta(days=weekday)).strftime("%Y-%m-%d")
        monday = '2020-09-14 00:00:00.000'
        result = execute_SQL(
            'voted_employees',
            'all',
            monday=monday,
            student_id=self.student_id
        )
        return [x[0].strip() for x in result]

    def sent_survey_today(self, query_type: str = 'standard'):
        #  def isStudentUsedToday(self, studentId):
        date = datetime.now().strftime
        result = execute_SQL(
            'is_student_used_today',
            'one',
            student_id=self.student_id, current_date=date,
            department_id=None if query_type == 'standard' else 9
        )
        return True if result else None

    
    def rate(self, employee: Employee, rating):
        #  def addSatisfication(self, studentId, employeeId, rank):
        execute_SQL(
            'add_satisfaction',
            'commit',
            student_id=self.student_id,
            department=employee.dep_number,
            employee_id=employee.card_id,
            rank=rating
        )

