class BaseController:
    
    def __init__(self):
        self._model = None
        self._view = None
    
    @property
    def model(self):
        return self._model
    
    @property
    def view(self):
        return self._view
    
    def refresh_view(self):
        if self._view and hasattr(self._view, 'refresh'):
            self._view.refresh()

    def handle_error(self, error, action):
        error_message = f"Lỗi {action}: {str(error)}"
        print(error_message)
