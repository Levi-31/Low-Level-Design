


class Rider:
    def __init__(self, rider_id: str, name: str, email: str, phone: str, created_at: int):
        self.id = rider_id
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = created_at

    def __repr__(self):
        return f"Rider(id={self.id!r}, name={self.name!r})"
    
    