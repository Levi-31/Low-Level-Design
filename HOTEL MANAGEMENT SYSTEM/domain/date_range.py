from dataclasses import dataclass

@dataclass
class DateRange:
    check_in_date_utc: int
    check_out_date_utc: int