from datetime import datetime
from .database import Database


class Classroom:
    def __init__(self) -> None:
        self.period = None
        pass

    def get_scheduled(self, period: int, date: str):
       
        result = Database.execute_SQL(
            'scheduled_classes', {'current_date': date, 'current_period': period}, 'all')
        classroom_map = ["", "301教室", "302教室", "303教室", "305教室", "會議室"]
        # [(2, '微積分B班(13)共補', '09:00', 1), (3, '微積分C班共補(8)', '09:00', 1)]
        result_dict_list = [{"location": classroom_map[t[0]], "name": t[1], "time": t[2], "other": t[3] } for t in result]
        print(result_dict_list)
