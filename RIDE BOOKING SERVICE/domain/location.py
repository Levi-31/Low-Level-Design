


class Location:
    def __init__(self, latitude: float = 0.0, longitude: float = 0.0,address: str = "", timestamp: int = 0):
        self.latitude =  latitude
        self.longitude = longitude
        self.address = address
        self.timestamp = timestamp

    def __repr__(self):
        return f"Location(lat={self.latitude}, lon={self.longitude}, addr={self.address!r})"