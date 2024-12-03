from .database import execute_SQL
from .student import Student


class Seat:
    def __init__(self, id: int = None) -> None:
        self.id = id
        self.is_taken = None
        pass

    def register_student(self, student: Student):
        # def add_class_seat_record(self, student_id, seat_id):
        execute_SQL(
            'add_student_seat','commit',student_id=student.student_id,
            seat_id=self.id
            
        )

    def is_taken(self, student: Student, class_id: int):
        #  def is_select_seat_today(self, student_id, class_id):
        self.is_taken = True if execute_SQL(
            'seat_taken',
            {
                "student_id": student.student_id,
                'class_id': class_id
            }
        ) else False

    def get_remaining(self):
        # def getSeatInfo(self):
        results = execute_SQL('remaining_seats', {}, 'all')
        results_dict = [{'name': t[0], 'male': t[1], 'female': t[2]}
                        for t in results]
        print(results_dict)

    @property
    def is_system_available(self):
        # def is_seat_system_available(self):
        return True if execute_SQL('seat_system_availability') else False
