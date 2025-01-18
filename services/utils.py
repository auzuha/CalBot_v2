import datetime, pytz


def get_ist_now():
    india_tz = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(india_tz)


def start_of_today_in_ist():
    india_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(india_tz)
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_today


