from .database import execute_SQL


class Student:

    def __init__(self, id) -> None:
        self.student_id = 0
        self.name = ''
        self.gender = None
        self._get_name_and_gender(id)

    def _get_name_and_gender(self, id):
        # def getStudentName(self, id):
        details = execute_SQL('student_details', {"id": id})
        self.student_id = details[0]
        self.name = details[1]

        if details[2] == '女':
            self.gender = 'female'
        elif details[2] == '男':
            self.gender = 'male'

    def get_classes(self):
        # def getClasses(self, id):
        classes = execute_SQL(
            'student_class', {"id": self.student_id}, 'all')
        # unknown method

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
