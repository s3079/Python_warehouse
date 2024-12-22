import tkinter as tk
from tkinter import ttk
from app.views.base_view import BaseView

class ProductView(BaseView):
    def _setup_ui(self):
        # Create main container
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tree view for products
        self.tree = ttk.Treeview(
            self.content_frame, 
            columns=("ID", "Name", "Description", "Price", "Category", "Supplier"),
            show="headings"
        )
        
        # Setup columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Supplier", text="Supplier")
        
        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Price", width=100)
        self.tree.column("Category", width=100)
        self.tree.column("Supplier", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create form frame
        self.form_frame = ttk.LabelFrame(self.frame, text="Product Details")
        self.form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create form fields
        # Name
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(self.form_frame, text="Description:").grid(row=0, column=2, padx=5, pady=5)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(self.form_frame, textvariable=self.desc_var)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Price
        ttk.Label(self.form_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(self.form_frame, textvariable=self.price_var)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Category
        ttk.Label(self.form_frame, text="Category:").grid(row=1, column=2, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.form_frame, textvariable=self.category_var)
        self.category_combo.grid(row=1, column=3, padx=5, pady=5)
        
        # Supplier
        ttk.Label(self.form_frame, text="Supplier:").grid(row=2, column=0, padx=5, pady=5)
        self.supplier_var = tk.StringVar()
        self.supplier_combo = ttk.Combobox(self.form_frame, textvariable=self.supplier_var)
        self.supplier_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add buttons
        ttk.Button(self.buttons_frame, text="Add", command=self._on_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Update", command=self._on_update).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Delete", command=self._on_delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Clear", command=self._on_clear).pack(side=tk.LEFT, padx=5)
        
        # Bind tree selection
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
    
    def refresh(self, products=None):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        if products:
            for product in products:
                self.tree.insert(
                    "", 
                    tk.END, 
                    values=(
                        product["product_id"],
                        product["name"],
                        product["description"],
                        f"{float(product['price']):.2f}",
                        product["category_name"] or "",
                        product["supplier_name"] or ""
                    )
                )
    
    def update_categories(self, categories):
        """Update category combobox values"""
        self.categories = {cat["name"]: cat["category_id"] for cat in categories}
        self.category_combo["values"] = list(self.categories.keys())
    
    def update_suppliers(self, suppliers):
        """Update supplier combobox values"""
        self.suppliers = {sup["name"]: sup["supplier_id"] for sup in suppliers}
        self.supplier_combo["values"] = list(self.suppliers.keys())
    
    def _on_add(self):
        if self.controller:
            try:
                price = float(self.price_var.get())
                category_id = self.categories.get(self.category_var.get())
                supplier_id = self.suppliers.get(self.supplier_var.get())
                
                self.controller.add_product(
                    self.name_var.get(),
                    self.desc_var.get(),
                    price,
                    category_id,
                    supplier_id
                )
            except ValueError as e:
                self.show_error("Invalid price format. Please enter a valid number.")
    
    def _on_update(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error("Please select a product to update")
            return
            
        if self.controller:
            try:
                product_id = self.tree.item(selected[0])["values"][0]
                price = float(self.price_var.get())
                category_id = self.categories.get(self.category_var.get())
                supplier_id = self.suppliers.get(self.supplier_var.get())
                
                self.controller.update_product(
                    product_id,
                    self.name_var.get(),
                    self.desc_var.get(),
                    price,
                    category_id,
                    supplier_id
                )
            except ValueError as e:
                self.show_error("Invalid price format. Please enter a valid number.")
    
    def _on_delete(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error("Please select a product to delete")
            return
            
        if self.controller:
            product_id = self.tree.item(selected[0])["values"][0]
            self.controller.delete_product(product_id)
    
    def _on_clear(self):
        """Clear all form fields"""
        self.name_var.set("")
        self.desc_var.set("")
        self.price_var.set("")
        self.category_var.set("")
        self.supplier_var.set("")
        
        # Deselect tree item
        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)
    
    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.name_var.set(values[1])
            self.desc_var.set(values[2])
            self.price_var.set(values[3])
            self.category_var.set(values[4])
            self.supplier_var.set(values[5])
