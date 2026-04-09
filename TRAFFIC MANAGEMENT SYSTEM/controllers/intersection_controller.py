


from domain.direction import Direction
from service.intersection_service import IntersectionService


class IntersectionController:
    def __init__(self,intersection_service: IntersectionService):
        self.intersection_service = intersection_service

        print("IntersectionController initialized")


    def create_intersection(self,id:int ,name:str):
        self.intersection_service.create_intersection(id,name)
    

    def get_intersection(self,intersection_id:int):
        self.intersection_service.get_intersection(intersection_id)
    

    def start_cycle(self,intersection_id):
        self.intersection_service.start_automatic_cycle(intersection_id)
    

    def display_status(self, intersection_id: int):
        intersection = self.get_intersection(intersection_id)
        if intersection:
            print(f"\n--- Intersection Status: {intersection.name} ---")
            print(intersection)
            for direction in Direction:
                light = intersection.get_traffic_light(direction)
                if light:
                    print(f"  {light}")
            cycle = self.intersection_service.get_cycle(intersection_id)
            if cycle:
                print(f"  {cycle}")
            print("------------------------------------------")
