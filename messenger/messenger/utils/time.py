import datetime


def get_good_part_of_day(utc_offset: int) -> str:
    hour = get_time_of_day(utc_offset)
    if 6 <= hour < 12:
        return 'Доброе утро'
    elif 12 <= hour < 19:
        return 'Добрый день'
    elif 19 <= hour < 24:
        return 'Добрый вечер'
    return 'Доброй ночи'


def get_time_of_day(utc_offset: int) -> int:
    delta = datetime.timedelta(hours=utc_offset) if utc_offset >= 0 \
        else -datetime.timedelta(hours=-utc_offset)
    return (datetime.datetime.utcnow() + delta).hour
