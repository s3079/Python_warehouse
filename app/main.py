import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk
from app.config.config import Config
from app.controllers.category_controller import CategoryController
from app.controllers.supplier_controller import SupplierController
from app.controllers.product_controller import ProductController
from app.controllers.inventory_controller import InventoryController
from app.utils.languages import LANGUAGES

class WarehouseApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_language = Config.DEFAULT_LANGUAGE
        self.setup_window()
        
    def setup_window(self):
        """Setup the main window"""
        self.root.title(self.translate('app_title'))
        self.root.geometry(Config.WINDOW_SIZE)
        
        # Create language selector
        self.create_language_selector()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Initialize controllers (they will create their own views)
        self.category_controller = CategoryController(self.notebook)
        self.supplier_controller = SupplierController(self.notebook)
        self.product_controller = ProductController(self.notebook)
        self.inventory_controller = InventoryController(self.notebook)
        
        # Add tabs
        self.notebook.add(self.category_controller.view.frame, text=self.translate('categories'))
        self.notebook.add(self.supplier_controller.view.frame, text=self.translate('suppliers'))
        self.notebook.add(self.product_controller.view.frame, text=self.translate('products'))
        self.notebook.add(self.inventory_controller.view.frame, text=self.translate('inventory'))
        
    def translate(self, key):
        """Translate a key to the current language"""
        return LANGUAGES[self.current_language][key]
        
    def create_language_selector(self):
        """Create the language selection dropdown"""
        language_frame = ttk.Frame(self.root)
        language_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(language_frame, text=self.translate('language') + ":").pack(side='left', padx=5)
        self.language_var = tk.StringVar(value=self.current_language)
        language_combo = ttk.Combobox(
            language_frame, 
            textvariable=self.language_var,
            values=list(LANGUAGES.keys()),
            state='readonly',
            width=20
        )
        language_combo.pack(side='left')
        language_combo.bind('<<ComboboxSelected>>', self.change_language)
    
    def change_language(self, event=None):
        """Handle language change"""
        self.current_language = self.language_var.get()
        # Update UI text
        self.root.title(self.translate('app_title'))
        
        # Update tab texts
        self.notebook.tab(0, text=self.translate('categories'))
        self.notebook.tab(1, text=self.translate('suppliers'))
        self.notebook.tab(2, text=self.translate('products'))
        self.notebook.tab(3, text=self.translate('inventory'))
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = WarehouseApp()
    app.run()
