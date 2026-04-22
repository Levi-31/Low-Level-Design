

from domain.building import Building
from domain.system_state import SystemState
from repository.building_repository import BuildingRepository


class BuildingService:
    def __init__(self, repository: BuildingRepository) -> None:
        self.building_repository = repository

    def create_building(self, name: str, min_floor: int, max_floor: int, total_elevators: int) -> Building:
        building = Building(name, min_floor, max_floor, total_elevators)
        return self.building_repository.save(building)


    def is_valid_floor(self, building_id: str, floor: int) -> bool:
        building = self.building_repository.find_by_id(building_id)
        return building.is_valid_floor(floor) if building else False
    
    def set_building_system_state(self, building_id: str, state: SystemState) -> None:
        building = self.building_repository.find_by_id(building_id)
        if building:
            building.system_state = state
            self.building_repository.save(building)

    def is_system_running(self, building_id: str) -> bool:
        building = self.building_repository.find_by_id(building_id)
        return building.system_state == SystemState.RUNNING if building else False
    
    def building_exists(self, building_id: str) -> bool:
        return self.building_repository.find_by_id(building_id) is not None