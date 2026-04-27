


from typing import List

from domain.document import Document
from domain.document_element import DocumentElement


class DocumentService:
    def __init__(self):
        self.document_elements : List[DocumentElement] = []
    

    def add_element(self,doc_element:DocumentElement):
        self.document_elements.append(doc_element)
    

    def get_all_elements(self) -> List[DocumentElement] :
        return list(self.document_elements)
