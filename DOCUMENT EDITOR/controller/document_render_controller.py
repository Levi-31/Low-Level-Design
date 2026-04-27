


from service.render_service import DocumentRenderService


class DocumentRenderController:
    def __init__(self,document_render_service:DocumentRenderService):
        self.document_render_service = document_render_service
    

    def render_document(self):
        return self.document_render_service.render_document()
        