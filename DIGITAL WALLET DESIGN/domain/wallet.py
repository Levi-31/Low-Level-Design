



from domain.wallet_status import WalletStatus


class Wallet:
    def __init__(self, id: str, account_number: str, balance_minor: int,
                 user_id: str, status: WalletStatus, created_at: int, updated_at: int):
        self._id = id
        self._account_number = account_number
        self._balance_minor = balance_minor
        self._user_id = user_id
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def account_number(self) -> str:
        return self._account_number

    @account_number.setter
    def account_number(self, value: str):
        self._account_number = value

    @property
    def balance_minor(self) -> int:
        return self._balance_minor

    @balance_minor.setter
    def balance_minor(self, value: int):
        self._balance_minor = value

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        self._user_id = value

    @property
    def status(self) -> WalletStatus:
        return self._status

    @status.setter
    def status(self, value: WalletStatus):
        self._status = value

    @property
    def created_at(self) -> int:
        return self._created_at

    @created_at.setter
    def created_at(self, value: int):
        self._created_at = value

    @property
    def updated_at(self) -> int:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: int):
        self._updated_at = value

    def __repr__(self) -> str:
        return (f"Wallet{{id='{self._id}', account_number='{self._account_number}', "
                f"balance_minor={self._balance_minor}, user_id='{self._user_id}', "
                f"status={self._status.name}}}")