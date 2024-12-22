import tkinter as tk
from tkinter import ttk
from app.views.base_view import BaseView

class InventoryView(BaseView):
    def _setup_ui(self):
        # Create main container
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tree view for inventory
        self.tree = ttk.Treeview(
            self.content_frame, 
            columns=("ID", "Product", "Category", "Supplier", "Quantity", "Price", "Total Value", "Last Updated"),
            show="headings"
        )
        
        # Setup columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Unit Price")
        self.tree.heading("Total Value", text="Total Value")
        self.tree.heading("Last Updated", text="Last Updated")
        
        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Product", width=150)
        self.tree.column("Category", width=100)
        self.tree.column("Supplier", width=100)
        self.tree.column("Quantity", width=80)
        self.tree.column("Price", width=100)
        self.tree.column("Total Value", width=100)
        self.tree.column("Last Updated", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create form frame
        self.form_frame = ttk.LabelFrame(self.frame, text="Update Inventory")
        self.form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create form fields
        # Product
        ttk.Label(self.form_frame, text="Product:").grid(row=0, column=0, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(self.form_frame, textvariable=self.product_var)
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Quantity
        ttk.Label(self.form_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
        self.quantity_var = tk.StringVar()
        self.quantity_entry = ttk.Entry(self.form_frame, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add buttons
        ttk.Button(self.buttons_frame, text="Update Quantity", 
                  command=self._on_update).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Show Low Stock", 
                  command=self._on_show_low_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Show All", 
                  command=self._on_show_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Clear", 
                  command=self._on_clear).pack(side=tk.LEFT, padx=5)
        
        # Bind tree selection
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
    
    def refresh(self, inventory=None):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        if inventory:
            for item in inventory:
                total_value = float(item['price']) * item['quantity']
                self.tree.insert(
                    "", 
                    tk.END, 
                    values=(
                        item["inventory_id"],
                        item["product_name"],
                        item["category_name"] or "",
                        item["supplier_name"] or "",
                        item["quantity"],
                        f"{float(item['price']):.2f}",
                        f"{total_value:.2f}",
                        item["last_updated"]
                    )
                )
    
    def update_products(self, products):
        """Update product combobox values"""
        self.products = {prod["name"]: prod["product_id"] for prod in products}
        self.product_combo["values"] = list(self.products.keys())
    
    def _on_update(self):
        if self.controller:
            try:
                product_id = self.products.get(self.product_var.get())
                quantity = int(self.quantity_var.get())
                
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative")
                    
                self.controller.update_inventory(product_id, quantity)
            except ValueError as e:
                self.show_error(str(e) if str(e) != "invalid literal for int() with base 10: ''" 
                              else "Please enter a valid quantity")
    
    def _on_show_low_stock(self):
        if self.controller:
            self.controller.show_low_stock()
    
    def _on_show_all(self):
        if self.controller:
            self.controller.refresh_view()
    
    def _on_clear(self):
        """Clear all form fields"""
        self.product_var.set("")
        self.quantity_var.set("")
        
        # Deselect tree item
        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)
    
    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.product_var.set(values[1])
            self.quantity_var.set(values[4])
