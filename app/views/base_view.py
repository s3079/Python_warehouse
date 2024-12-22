import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

class BaseView(ABC):
    """Abstract base class for all views"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self._controller = None
        self._setup_ui()
    
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
    def refresh(self, data=None):
        """Refresh the view with new data"""
        pass
    
    def show_error(self, message: str):
        """Show error message to user"""
        messagebox.showerror("Error", message)
    
    def show_success(self, message: str):
        """Show success message to user"""
        messagebox.showinfo("Success", message)
    
    def show(self):
        """Show the view"""
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Hide the view"""
        self.frame.pack_forget()
