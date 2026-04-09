class InvalidStateTransitionException(Exception):
    def __init__(self, from_state: str, to_state: str):
        super().__init__(f"Invalid state transition from {from_state} to {to_state}")