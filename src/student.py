from .database import execute_SQL
from datetime import datetime, timedelta


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

    def __init__(self, card_id) -> None:
        self.student_id = 0
        self.name = None
        self.gender = None
        self.classes = None
        self._get_name_and_gender(card_id)
        self._get_classes()

    def _get_name_and_gender(self, card_id):
        # def getStudentName(self, id):
        details = execute_SQL(
            'student_details',
            card_id=card_id
        )
        self.student_id = details[0]
        self.name = details[1]

        if details[2] == '女':
            self.gender = 'female'
        elif details[2] == '男':
            self.gender = 'male'

    def _get_classes(self):
        # def getClasses(self, id):
        if self.student_id is not None:
            self.classes = execute_SQL(
                'get_classes',
                'all',
                student_id=self.student_id
            )


    def selected_seat(self, class_id: int):
        #  def is_select_seat_today(self, student_id, class_id):
        return True if execute_SQL(
            'selected_seat',
            'one',
            student_id=self.student_id,
            class_id=class_id

        ) else False
    
    
    def get_seats(self, classroom_id: int):
        # getSeats(self, classroom_id):
        if self.gender == 'female':
            param = 'student_seats_female'
        elif self.gender == 'male':
            param = 'student_seats_male'
        else:
            print('ERROR: Attempting to get seats without gender')
            return
        result = execute_SQL(param, {
            'classroom_id': classroom_id
        }, 'all')
        result_dict = [
            {
                "sn": t[0],
                "seat_num": t[2],
                "student_id": t[3],
                "register_time": t[4]
            }
            for t in result
        ]

        return result_dict

    def register_student(self, seat_id):
        # def add_class_seat_record(self, student_id, seat_id):
        execute_SQL(
            'add_student_seat', 'commit', student_id=self.student_id,
            seat_id=seat_id

        )

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

    def get_available_selection(self):
        weekday = datetime.now().weekday()
        monday = (datetime.now() - timedelta(days=weekday)
                  ).strftime("%Y-%m-%d")
        results = execute_SQL(
            'get_available_selection',
            'all',
            monday=monday,
            student_id=self.id
        )
        # sql_res = [i[0] for i in [2, 3, 4, 5]]
        # return [x for x in [2, 3, 4, 5] if x not in sql_res]
