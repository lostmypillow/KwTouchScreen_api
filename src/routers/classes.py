from fastapi import APIRouter
from ..database import execute_SQL

router = APIRouter(
    prefix="/classes",
    tags=["Classes"],
)

@router.get('/{period}')
def get_classes(period: int):
    # date = datetime.now().strftime('%Y/%m/%d')
    date = '2023/08/15'
    result = execute_SQL(
        'scheduled_classes',
        'all',
        current_date=date, current_period=period
    )
    classroom_map = [
        "301教室",
        "302教室",
        "303教室",
        "305教室",
        "會議室"
    ]
    # [(2, '微積分B班(13)共補', '09:00', 1), (3, '微積分C班共補(8)', '09:00', 1)]
    return [
        {
            "location": classroom_map[t[0]-1],
            "name": t[1],
            "time": t[2],
            "other": t[3]
        } for t in result
    ]

