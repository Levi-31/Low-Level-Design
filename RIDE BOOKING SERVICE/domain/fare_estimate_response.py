



class FareEstimateResponse:
    def __init__(self, estimated_fare: int, distance_km: float,duration_sec: int, currency: str):
        self.estimated_fare = estimated_fare
        self.distance_km = distance_km
        self.duration_sec = duration_sec
        self.currency = currency