from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseController(ABC):
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
    
    @abstractmethod
    def initialize(self):
        """Initialize the controller"""
        pass
    
    @abstractmethod
    def refresh_view(self):
        """Refresh the view with updated data"""
        pass
    
    def handle_error(self, error: Exception, context: str = ""):
        """Handle errors in a consistent way"""
        error_message = f"Error in {context}: {str(error)}"
        # Log error here if needed
        if self._view:
            self._view.show_error(error_message)
