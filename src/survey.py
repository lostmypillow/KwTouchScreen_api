from .database import execute_SQL
class Survey:
    def __init__(self) -> None:
        pass
    def add_satisfaction(student_id, employee_id, rank, department):
    #  def addSatisfication(self, studentId, employeeId, rank):
     execute_SQL(
          'add_satisfaction', 
          'commit',student_id=student_id, department=department, employee_id=employee_id,
          rank=rank
        )