from typing import Optional

from domain.Vehicle import Vehicle
from domain.ticket import Ticket
from repository.ticket_repository import TicketRepository


class TicketService:
    def __init__(self, ticket_repository: TicketRepository):
        self._ticket_repository = ticket_repository

    def generate_ticket(self, vehicle: Vehicle, slot_id: str) -> Ticket:
        ticket = Ticket(vehicle.id, slot_id)
        return self._ticket_repository.save(ticket)

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        return self._ticket_repository.find_by_id(ticket_id)

    def deactivate_ticket(self, ticket_id: str):
        self._ticket_repository.deactivate_ticket(ticket_id) 
