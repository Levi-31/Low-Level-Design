from domain.document_element import ImageElement, NewLineElement, TextElement, TabSpaceElement
from service.document_service import DocumentService
from service.lock_service import LockService


class DocumentEditorService:
    def __init__(self, document_service: DocumentService, lock_service: LockService):
        self.document_service = document_service
        self.lock_service = lock_service

    def add_text(self, text: str):
        self.lock_service.acquire_lock()
        try:
            self.document_service.add_element(TextElement(text))
        finally:
            self.lock_service.release_lock()
    
    def add_image(self, image_path: str):
        self.lock_service.acquire_lock()
        try:
            self.document_service.add_element(ImageElement(image_path))
        finally:
            self.lock_service.release_lock()
    
    def add_new_line(self):
        self.lock_service.acquire_lock()
        try:
            self.document_service.add_element(NewLineElement())
        finally:
            self.lock_service.release_lock()

    def add_tab_space(self):
        self.lock_service.acquire_lock()
        try:
            self.document_service.add_element(TabSpaceElement())
        finally:
            self.lock_service.release_lock()