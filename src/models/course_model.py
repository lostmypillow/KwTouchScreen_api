from ..database import execute_SQL
from ..models.student_model import Student


class Course:

    def __init__(self):
        self.main_number = None
        self.male_seats = []
        self.female_seats = []
        self.name = None
        self.other_name = None
        self.seats = None
        self._check_availability()
        self._get_seats()

    def _check_availability(self):
        # def getSeatInfo(self):
        # def is_seat_system_available(self):
        result = execute_SQL('seats/remaining', 'one')
        if result:
            self.main_number = result[0]
            self.name = result[3]
            self.other_name = result[4]
    def _get_seats(self):
        results = execute_SQL('course/get_remaining_seats', 'all')
        print(results)
        if results:
            for res in results:
                if int(res[1][1:]) <= 15:
                    self.female_seats.append({"sn":res[0], "name": res[1]})
                else:
                    self.male_seats.append({"sn":res[0], "name": res[1]})


            
        print(len(results))

    def register_student(self, student: Student):
        execute_SQL('student/register_seat',
                    'commit',
                    student_id=student.student_id,
                    sn=self.class_details.sn
                    )
    @property
    def is_available(self):
        return bool(self.male_seats and self.female_seats)
        
