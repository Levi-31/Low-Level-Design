


from domain.location import Location
from domain.payment_type import PaymentType


class RideRequest:
    def __init__(self, rider_id: str, pickup_location: Location, dropoff_location: Location, payment_type: PaymentType):
        self.rider_id = rider_id
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.payment_type = payment_type