import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

class BaseView(ttk.Frame):
    """Abstract base class for all views"""
    
    def __init__(self, parent=None):
        """Initialize base view"""
        super().__init__(parent)
        self.parent = parent
        self.controller = None
        
        # Setup grid
        self.grid(sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        self._setup_ui()  # Call setup_ui directly
    
    @property
    def controller(self):
        return self._controller
    
    @controller.setter
    def controller(self, controller):
        self._controller = controller
    
    @abstractmethod
    def _setup_ui(self):
        """Set up the UI components"""
        pass
    
    @abstractmethod
    def refresh_view(self, data=None):
        """Refresh the view with new data"""
        pass
    
    def show_error(self, title, message):
        """Show error message to user"""
        messagebox.showerror(title, message)
    
    def show_info(self, title, message):
        """Show info message to user"""
        messagebox.showinfo(title, message)
    
    def show_warning(self, title, message):
        """Show warning message to user"""
        messagebox.showwarning(title, message)
    
    def show_confirmation(self, title, message):
        """Show confirmation dialog"""
        return messagebox.askyesno(title, message)
