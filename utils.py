import datetime

_UTC_OFFSET_TIMEDELTA = (datetime.datetime.utcnow() - datetime.datetime.now()).total_seconds()


def datetime_to_unix(date_time):
    return datetime.datetime.timestamp(date_time)
