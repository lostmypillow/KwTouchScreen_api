from typing import Any, Union
from app.database.async_operations import exec_sql
from app.routers.ws import active_connections


async def send_updates():

    # current_date = datetime.now().strftime('%Y/%m/%d')
    # current_hour = datetime.now().hour
    # match current_hour:
    #     case h if 12 <= h <= 17:
    #         current_period = 2
    #     case h if h <= 11:
    #         current_period = 1
    #     case _:
    #         current_period = 3

    current_date = '2023/08/15'  # DEBUG USE
    current_period = 1  # DEBUG USE

    classes_today: list[dict[str, Any]] = await exec_sql(
        'all',
        'classes_today',
        current_date=current_date,
        current_period=current_period
    )

    classroom_map = [
        "301教室",
        "302教室",
        "303教室",
        "305教室",
        "會議室"
    ]
    for c in classes_today:
        c['教室'] = classroom_map[c['教室'] - 1]


    # '位子'
    class_with_seats: dict[str, Union[str, list[str]]] = await exec_sql('one', 'single_get_remaining')

    # convert 位子, which is a string with a lot of commas, into a list
    # SQ.座位號,
    # SQ.座位
    class_with_seats['座位'] = [
        {"座位": seat, "號碼": seat_num}
        for seat, seat_num in zip(
            class_with_seats['座位'].split(','),
            class_with_seats['座位號'].split(',')
        )
    ]

    class_with_seats['男座位'] = []
    class_with_seats['女座位'] = []
    for seat in class_with_seats['座位']:
        if int(seat["座位"][-2:]) <= 15:
            class_with_seats['女座位'].append(seat)
        else:
            class_with_seats['男座位'].append(seat)
            
    del class_with_seats['座位']
    del class_with_seats['座位號']


    data = {
        "classes_today": classes_today,
        "class_with_seats": class_with_seats
    }
    

    if active_connections:
        for con in active_connections:
            await active_connections[con].send_json(
                {
                    "action": "update class",
                    "message": data
                }
            )
