import threading
import time
from domain.persistence import FileStorage
from service.document_service import DocumentService
from service.document_editor_service import DocumentEditorService
from service.render_service import DocumentRenderService
from service.storage_service import DocumentStorageService
from service.lock_service import LockService
from controller.document_editor_controller import DocumentEditorController
from controller.document_render_controller import DocumentRenderController
from controller.storage_controller import DocumentStorageController

def simulate_user_edit(controller: DocumentEditorController, name: str):
    print(f"\\n--- {name} editing ---")
    controller.add_text(f"Hello from {name}! ")
    controller.add_new_line()
    print(f"{name} finished editing.")

if __name__ == "__main__":
    # Initialize Core Services / Repositories
    document_service = DocumentService()
    persistence = FileStorage()
    lock_service = LockService()
    
    # Initialize Application Services
    editor_service = DocumentEditorService(document_service, lock_service)
    render_service = DocumentRenderService(document_service)
    storage_service = DocumentStorageService(persistence)
    
    # Initialize Controllers
    editor_controller = DocumentEditorController(editor_service)
    render_controller = DocumentRenderController(render_service)
    storage_controller = DocumentStorageController(storage_service)
    
    # Simulate concurrent editing by multiple users
    t1 = threading.Thread(target=simulate_user_edit, args=(editor_controller, "User 1"))
    t2 = threading.Thread(target=simulate_user_edit, args=(editor_controller, "User 2"))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

    # Render and display the final document.
    print("\\n--- Final Document ---")
    rendered_doc = render_controller.render_document()
    print(rendered_doc)
    
    # Save the document
    storage_controller.save_document(rendered_doc)
