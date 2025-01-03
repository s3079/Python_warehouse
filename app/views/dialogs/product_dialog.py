import tkinter as tk
from tkinter import ttk, messagebox

class ProductDialog:
    def __init__(self, parent, title, categories=None, suppliers=None, initial_data=None):
        self.result = None
        self.categories = categories or []
        self.suppliers = suppliers or []
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        window_width = 400
        window_height = 400
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar(value=initial_data['name'] if initial_data else "")
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_var = tk.StringVar(value=initial_data['description'] if initial_data else "")
        self.desc_entry = ttk.Entry(main_frame, textvariable=self.desc_var)
        self.desc_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Unit Price
        ttk.Label(main_frame, text="Unit Price:").grid(row=2, column=0, sticky="w", pady=5)
        self.price_var = tk.StringVar(value=str(initial_data['unit_price']) if initial_data else "0.00")
        self.price_entry = ttk.Entry(main_frame, textvariable=self.price_var)
        self.price_entry.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Category
        ttk.Label(main_frame, text="Category:").grid(row=3, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar(value=initial_data['category_id'] if initial_data else "")
        self.category_combo = ttk.Combobox(main_frame, textvariable=self.category_var)
        self.category_combo['values'] = [f"{c['category_id']} - {c['name']}" for c in self.categories]
        self.category_combo.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Supplier
        ttk.Label(main_frame, text="Supplier:").grid(row=4, column=0, sticky="w", pady=5)
        self.supplier_var = tk.StringVar(value=initial_data['supplier_id'] if initial_data else "")
        self.supplier_combo = ttk.Combobox(main_frame, textvariable=self.supplier_var)
        self.supplier_combo['values'] = [f"{s['supplier_id']} - {s['name']}" for s in self.suppliers]
        self.supplier_combo.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        
        # Make dialog modal
        self.dialog.wait_window()
    
    def _on_ok(self):
        """Handle OK button click"""
        name = self.name_var.get().strip()
        description = self.desc_var.get().strip()
        price = self.price_var.get().strip()
        category = self.category_var.get().strip()
        supplier = self.supplier_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        
        try:
            price = float(price)
            if price < 0:
                raise ValueError("Price must be positive")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        # Extract IDs from combobox values
        category_id = int(category.split(' - ')[0]) if category else None
        supplier_id = int(supplier.split(' - ')[0]) if supplier else None
        
        self.result = {
            'name': name,
            'description': description,
            'unit_price': price,
            'category_id': category_id,
            'supplier_id': supplier_id
        }
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button click"""
        self.dialog.destroy()
