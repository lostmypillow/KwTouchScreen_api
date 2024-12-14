from .database import execute_SQL
from .student import Student


class Course:

    def __init__(self):
        self.has_seats = False
        self.main_number = None
        self.male_seats = None
        self.female_seats = None
        self.name = None
        self.other_name = None
        self.seats = None
        self._check_availability()
        self.get_seats()

    def _check_availability(self):
        # def getSeatInfo(self):
        # def is_seat_system_available(self):
        result = execute_SQL('seats/remaining', 'one')
        if result:
            self.has_seats = True
            self.main_number = result[0]
            self.name = result[3]
            self.other_name = result[4]
    def get_seats(self):
        self.seats = []
        results = execute_SQL('course/get_remaining_seats', 'all')
        for res in results:
            if int(res[1])
            self.seats.append({"sn":res[0], "name": res[1]})
            
        print(len(results))

    def register_student(self, student: Student):
        execute_SQL('student/register_seat',
                    'commit',
                    student_id=student.student_id,
                    sn=self.class_details.sn
                    )
        
    @property
    def male_seats_number(self):
        return ""
