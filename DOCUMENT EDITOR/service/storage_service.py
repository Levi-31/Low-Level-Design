from domain.persistence import Persistence

class DocumentStorageService:
    def __init__(self, storage: Persistence):
        self.storage = storage

    def save_document(self, data: str):
        self.storage.save(data)
