from models.course_model import Course

def get_class_with_seat():
    # def getSeatInfo(self):
    # def is_seat_system_available(self):
    course = Course()
    return {
        "type": "remaining",
        "data": course.model_dump()
    }
