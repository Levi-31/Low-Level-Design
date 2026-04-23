

from typing import Optional

from domain.driver_status import DriverStatus
from domain.location import Location


class Driver:
    def __init__(self, driver_id: str, name: str, email: str, phone: str,vehicle_number: str, vehicle_type: str, status: DriverStatus):
        self.id = driver_id
        self.name = name
        self.email = email
        self.phone = phone
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.status = status
        self.current_location: Optional[Location] = None
        self.last_location_update: int = 0

    def __repr__(self):
        return f"Driver(id={self.id!r}, name={self.name!r}, status={self.status})"