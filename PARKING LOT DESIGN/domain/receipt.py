from datetime import datetime
from enum import Enum
import uuid


class Receipt:
    class PaymentStatus(Enum):
        PENDING= "PENDING"
        SUCCESS = "SUCCESS"
        FAIL = "FAIL"

    def __int__(self,ticket_id:str,total_fees :float):
        self.id = uuid.uuid4()
        self.ticket_id = ticket_id
        self.exit_time = datetime.now()
        self.total_fees : float = total_fees
        self.payment_status = self.PaymentStatus.PENDING

    def mark_as_paid(self):
        self.payment_status = self.PaymentStatus.SUCCESS
