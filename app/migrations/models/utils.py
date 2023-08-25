from datetime import date, datetime, timedelta


def get_current_time() -> datetime:
    return datetime.utcnow() + timedelta(hours=7)

def get_yesterday():
    my_date = get_current_time()
    today = date(day=my_date.day, month=my_date.month, year=my_date.year)
    return today - timedelta(days=1)

def get_yesterday_from_a_day(today: date = date.today()):
    return today - timedelta(days=1)
