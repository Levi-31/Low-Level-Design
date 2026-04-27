from service.storage_service import DocumentStorageService

class DocumentStorageController:
    def __init__(self, storage_service: DocumentStorageService):
        self.storage_service = storage_service

    def save_document(self, data: str):
        self.storage_service.save_document(data)
