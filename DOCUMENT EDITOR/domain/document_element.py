



from abc import ABC , abstractmethod


class DocumentElement(ABC):
    @abstractmethod
    def render(self):
        pass


class TextElement(DocumentElement):
    def __init__(self,text:str):
        self.text = text


    def render(self):
        return self.text



class ImageElement(DocumentElement):
    def __init__(self,image_path:str):
        self.image_path = image_path


    def render(self):
        return f"[Image: {self.image_path}]"



class NewLineElement(DocumentElement):

    def render(self):
        return "\n"


class TabSpaceElement(DocumentElement):

    def render(self):
        return "\t"


    