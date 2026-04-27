from service.document_editor_service import DocumentEditorService

class DocumentEditorController:
    def __init__(self, document_editor_service: DocumentEditorService):
        self.document_editor_service = document_editor_service

    def add_text(self, text: str):
        self.document_editor_service.add_text(text)

    def add_image(self, image_path: str):
        self.document_editor_service.add_image(image_path)

    def add_new_line(self):
        self.document_editor_service.add_new_line()
    
    def add_tab_space(self):
        self.document_editor_service.add_tab_space()
