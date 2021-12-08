import datetime
import time

UTC_TIMEZONE = datetime.timezone.utc

INITIAL_DATE = datetime.datetime(
    year = 1970,
    month = 1,
    day = 1,
    hour = 0,
    minute = 0,
    second = 0,
    tzinfo = UTC_TIMEZONE
    )

DELTA_ONE_MONTH = 2592000000 # one moth duration in miliseconds
DELTA_SIX_MONTHS = DELTA_ONE_MONTH*6
DELTA_SEVEN_MONTHS = DELTA_ONE_MONTH*7
DELTA_THIRTEEN_MONTHS = DELTA_ONE_MONTH*13

def delta_to_miliseconds(delta) -> int:
    return int(delta.total_seconds()*1000)

def delta_miliseconds(from_date: datetime.datetime, to_date: datetime.datetime) -> int:
    delta = from_date - to_date
    delta_miliseconds = delta_to_miliseconds(delta)
    return delta_miliseconds

def now() -> datetime.datetime:
    return datetime.datetime.now(tz=UTC_TIMEZONE)

def datetime_from_now(days=0, hours=0, minutes=0) -> datetime.datetime:
    current = now()
    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return current - delta

def miliseconds_from_initial(date: datetime.datetime) -> int:
    date = date.replace(tzinfo=UTC_TIMEZONE)
    return delta_miliseconds(date, INITIAL_DATE)

class TimeGuard(object):
    """
    Managing time and helps to keep specific time interval (with possible offset) between calls.
    Eg. when created with interval of 10 minutes in real time of 16:03
    it will next pass on 16:10 and then on 16:20 and so on.
    if eg. offset is set to 5 sec it will pass on 16:10:05 and then on 16:20:05.
    Thread will be put to sleep until time condition will not pass.
    """
    def __init__(self, interval: datetime.datetime, offset = datetime.timedelta(seconds=0)):
        self._interval = delta_to_miliseconds(interval)
        self._offset = delta_to_miliseconds(offset)

    def start(self):
        current_timestamp = miliseconds_from_initial(now())
        nearest_interval_begin = current_timestamp % self._interval
        self._nearest_unlock_timestamp = current_timestamp + self._interval - nearest_interval_begin

    def passed(self):
        current_timestamp = miliseconds_from_initial(now())
        if current_timestamp > self._nearest_unlock_timestamp + self._offset:
            self._nearest_unlock_timestamp = self._nearest_unlock_timestamp + self._interval
            return True
        delay_ms = self._nearest_unlock_timestamp + self._offset - current_timestamp
        time.sleep(delay_ms/1000)
        return True