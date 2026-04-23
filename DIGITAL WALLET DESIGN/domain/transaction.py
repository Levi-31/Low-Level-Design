



from domain.transaction_status import TransactionStatus
from domain.transaction_type import TransactionType


class Transaction:
    def __init__(self, id: str, from_wallet_id: str, to_wallet_id: str,
                 amount_minor: int, type_: TransactionType, status: TransactionStatus,
                 provider_ref: str, description: str, timestamp: int):
        self._id = id
        self._from_wallet_id = from_wallet_id  # empty string for DEPOSIT
        self._to_wallet_id = to_wallet_id       # empty string for WITHDRAWAL
        self._amount_minor = amount_minor
        self._type = type_
        self._status = status
        self._provider_ref = provider_ref       # empty string if not applicable
        self._description = description
        self._timestamp = timestamp

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def from_wallet_id(self) -> str:
        return self._from_wallet_id

    @from_wallet_id.setter
    def from_wallet_id(self, value: str):
        self._from_wallet_id = value

    @property
    def to_wallet_id(self) -> str:
        return self._to_wallet_id

    @to_wallet_id.setter
    def to_wallet_id(self, value: str):
        self._to_wallet_id = value

    @property
    def amount_minor(self) -> int:
        return self._amount_minor

    @amount_minor.setter
    def amount_minor(self, value: int):
        self._amount_minor = value

    @property
    def type(self) -> TransactionType:
        return self._type

    @type.setter
    def type(self, value: TransactionType):
        self._type = value

    @property
    def status(self) -> TransactionStatus:
        return self._status

    @status.setter
    def status(self, value: TransactionStatus):
        self._status = value

    @property
    def provider_ref(self) -> str:
        return self._provider_ref

    @provider_ref.setter
    def provider_ref(self, value: str):
        self._provider_ref = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: int):
        self._timestamp = value

    def __repr__(self) -> str:
        return (f"Transaction{{id='{self._id}', from_wallet_id='{self._from_wallet_id}', "
                f"to_wallet_id='{self._to_wallet_id}', amount_minor={self._amount_minor}, "
                f"type={self._type.name}, status={self._status.name}}}")
