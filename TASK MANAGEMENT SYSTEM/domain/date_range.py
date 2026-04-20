from datetime import datetime

class DateRange:
    def __init__(self, start_date: datetime, end_date: datetime):
        self._start_date = start_date
        self._end_date = end_date

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date
