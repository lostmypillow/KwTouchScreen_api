from datetime import datetime
from database.operations import fetch_all_sql
import asyncio
import json


def get_today_classes():
    while True:
        # date = datetime.now().strftime('%Y/%m/%d')
        # current_hour = datetime.now().hour
        # match current_hour:
        #     case h if 12 <= h <= 17:
        #         period = 2
        #     case h if h <= 11:
        #         period = 1
        #     case _:
        #         period = 3

        current_date = '2023/08/15'  # DEBUG USE
        current_hour = 7 # DEBUG USE
        current_period = 1  # DEBUG USE


        converted_list = []
        data_keys = ('location', 'name', 'time', 'other')

        results = fetch_all_sql(
            'scheduled_classes',
            current_date=date,
            current_period=period
        )
        print(results)

        for result in results:

            extracted_hour = datetime.strptime(result[2], "%H:%M").hour
            print(f"extracted hour: {extracted_hour}")

            if extracted_hour > current_hour:

                result_dict = {
                    data_keys[i]: result[i]
                    for i, _ in enumerate(result)
                }

                result_dict['教室'] = [
                    "301教室",
                    "302教室",
                    "303教室",
                    "305教室",
                    "會議室"
                ][result_dict['教室'] - 1]

                converted_list.append(result_dict)
        return converted_list
#  [
#   {
#     "教室": 2,
#     "內容": "微積分B班(13)共補",
#     "時間": "09:00",
#     "共補": 1
#   },
#   {
#     "教室": 3,
#     "內容": "微積分C班共補(8)",
#     "時間": "09:00",
#     "共補": 1
#   }
# ]
