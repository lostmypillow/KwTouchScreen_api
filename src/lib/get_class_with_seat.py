from models.course_model import Course
from database.operations import fetch_one_sql, fetch_all_sql

data = {
    "male_seats": [],
    "female_seats": [],
    "name": "",
    "other_name": "",
    "seats": 0
}


def get_class_with_seat():
    # def getSeatInfo(self):
    # def is_seat_system_available(self):
    # course = Course()
    # return {
    #     "type": "remaining",
    #     "data": course.model_dump()
    # }

    class_data = fetch_one_sql('seats/remaining')
    all_seats = fetch_all_sql('course/get_remaining_seats')
    if class_data and all_seats:
        data['main_number'] = class_data[0]
        data['name'] = class_data[3]
        data['other_name'] = class_data[4]
        data['female_seats'] = [
            {
                "sn": seat[0],
                "name": seat[1]
            }
            for seat in all_seats if int(seat[1][1:]) <= 15
        ]
        data['male_seats'] = [
            {
                "sn": seat[0],
                "name": seat[1]
            }
            for seat in all_seats if int(seat[1][1:]) > 15
        ]
        return data
    else:
        return None

