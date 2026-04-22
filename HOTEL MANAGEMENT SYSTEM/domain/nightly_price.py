


from dataclasses import dataclass

@dataclass
class NightlyPrice:
    date_utc: int
    price_minor: int