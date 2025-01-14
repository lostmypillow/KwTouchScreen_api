from datetime import datetime
from database.operations import fetch_all_sql
def get_today_classes():
    date = datetime.now().strftime('%Y/%m/%d')
    classroom_map = [
        "301教室",
        "302教室",
        "303教室",
        "305教室",
        "會議室"
    ]

    converted_list = []
    data_keys = ('location', 'name', 'time', 'other')
    

    if current_hour >= 12 and current_hour <= 17:
        period = 2
    elif current_hour <= 11:
        period = 1
    else:
        period = 3

    results = fetch_all_sql(
        'scheduled_classes',
        current_date=date,
        current_period=period
    )

    for result in results:
        extracted_hour = datetime.strptime(result[2], "%H:%M").hour
        current_hour = datetime.now().hour
        if extracted_hour > current_hour:
            result_dict = {data_keys[i]: result[i]
                           for i, _ in enumerate(result)}
            result_dict['location'] = classroom_map[result_dict['location'] - 1]
            converted_list.append(result_dict)
    return {
        "type": "today",
        "data": converted_list
    }
    # [(2, '微積分B班(13)共補', '09:00', 1), (3, '微積分C班共補(8)', '09:00', 1)]
