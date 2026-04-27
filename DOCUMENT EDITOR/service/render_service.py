


from domain.document import Document
from service.document_service import DocumentService


class DocumentRenderService:
    def __init__(self,doc_service:DocumentService):
        self.doc_service = doc_service
    

    def render_document(self):
        doc_elements = self.doc_service.get_all_elements()

        result = ""
        if doc_elements:
            for doc_element in doc_elements:
                result+= doc_element.render()
            
            return result

        else:
            raise Exception("Empty Document")
        
