from typing import Dict, List, Optional
from domain.recovery import Recovery
from domain.recovery_status import RecoveryStatus

class RecoveryRepository:
    def __init__(self):
        self._recoveries: Dict[int, Recovery] = {}

    def save(self, recovery: Recovery):
        self._recoveries[recovery.id] = recovery

    def find_by_machine_id(self, machine_id: int) -> Optional[Recovery]:
        for r in self._recoveries.values():
            if r.vending_machine_id == machine_id:
                return r
        return None

    def find_pending_by_machine_id(self, machine_id: int) -> List[Recovery]:
        return [r for r in self._recoveries.values() if r.vending_machine_id == machine_id and r.status == RecoveryStatus.PENDING]
