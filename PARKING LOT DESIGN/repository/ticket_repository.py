

from typing import Dict, List, Optional

from domain.ticket import Ticket


class TicketRepository:
    def __init__(self):
        self._tickets: Dict[str, Ticket] = {}
    

    def save(self, ticket: Ticket) -> Ticket:
        self._tickets[ticket.id] = ticket
        return ticket
    
    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        return self._tickets.get(ticket_id)
    
    def find_active_tickets(self) -> List[Ticket]:
        return [ticket for ticket in self._tickets.values() if ticket.is_active]
    
    def deactivate_ticket(self, ticket_id: str):
        ticket = self._tickets.get(ticket_id)
        if ticket:
            ticket.deactivate()

    def clear(self):
        self._tickets.clear()

        
    
