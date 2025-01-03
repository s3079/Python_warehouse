import tkinter as tk
from tkinter import ttk, messagebox

class InventoryDialog(tk.Toplevel):
    def __init__(self, parent=None, products=None, initial_data=None):
        super().__init__(parent)
        self.products = products or []
        self.initial_data = initial_data
        self.title("Inventory")
        self.minsize(400, 300)
        self.result = None
        self._setup_ui()
        
    def _setup_ui(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Form fields
        current_row = 0
        
        # Product
        ttk.Label(main_frame, text="Product:").grid(row=current_row, column=0, sticky="w", pady=(0, 5))
        current_row += 1
        self.product_var = tk.StringVar(value=self.initial_data.get('product_id', '') if self.initial_data else '')
        self.product_combo = ttk.Combobox(main_frame, textvariable=self.product_var)
        self.product_combo['values'] = [f"{p['name']}" for p in self.products]
        if self.initial_data and 'product_id' in self.initial_data:
            index = [p['name'] for p in self.products].index([p['name'] for p in self.products if p['product_id'] == self.initial_data['product_id']][0])
            self.product_combo.current(index)
        self.product_combo.grid(row=current_row, column=0, sticky="ew", pady=(0, 10))
        current_row += 1
        
        # Quantity
        ttk.Label(main_frame, text="Quantity:").grid(row=current_row, column=0, sticky="w", pady=(0, 5))
        current_row += 1
        self.quantity_var = tk.StringVar(value=str(self.initial_data.get('quantity', '')) if self.initial_data else '')
        self.quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=current_row, column=0, sticky="ew", pady=(0, 10))
        current_row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=current_row, column=0, sticky="ew", pady=(10, 0))
        button_frame.grid_columnconfigure(1, weight=1)
        
        save_btn = ttk.Button(button_frame, text="Save", command=self._on_save)
        save_btn.grid(row=0, column=0, padx=(0, 5))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_btn.grid(row=0, column=1, padx=(5, 0))
        
    def _on_save(self):
        try:
            quantity = int(self.quantity_var.get())
            if quantity < 0:
                raise ValueError("Quantity must be positive")
                
            self.result = {
                'product_id': [p['product_id'] for p in self.products if p['name'] == self.product_var.get()][0],
                'quantity': quantity
            }
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def set_products(self, products):
        """Set the list of available products"""
        self.product_combo['values'] = [f"{p['name']}" for p in products]
