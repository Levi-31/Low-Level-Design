


from typing import Dict, List, Optional

from domain.building import Building


class BuildingRepository:
    def __init__(self):
        self._buildings:Dict[str , Building] = {}

    def save(self, building: Building) -> Building:
        self._buildings[building.id] = building
        return building

    def find_by_id(self, building_id: str) -> Optional[Building]:
        return self._buildings.get(building_id)

    def find_all(self) -> List[Building]:
        return list(self._buildings.values())