class BaseController:
    """Abstract base class for all controllers"""
    
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
        """Refresh the view with current data"""
        if self._view and hasattr(self._view, 'refresh'):
            self._view.refresh()

    def handle_error(self, error, action):
        """Handle errors in the controller"""
        error_message = f"Error {action}: {str(error)}"
        print(error_message)  # Log the error
