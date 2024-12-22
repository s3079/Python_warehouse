import tkinter as tk
from tkinter import ttk
from app.views.base_view import BaseView

class SupplierView(BaseView):
    def _setup_ui(self):
        # Create main container
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tree view for suppliers
        self.tree = ttk.Treeview(
            self.content_frame, 
            columns=("ID", "Name", "Contact", "Address", "Phone", "Email"),
            show="headings"
        )
        
        # Setup columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact", text="Contact Name")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        
        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Contact", width=150)
        self.tree.column("Address", width=200)
        self.tree.column("Phone", width=100)
        self.tree.column("Email", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create form frame
        self.form_frame = ttk.LabelFrame(self.frame, text="Supplier Details")
        self.form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create form fields
        # Name
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Contact Name
        ttk.Label(self.form_frame, text="Contact Name:").grid(row=0, column=2, padx=5, pady=5)
        self.contact_var = tk.StringVar()
        self.contact_entry = ttk.Entry(self.form_frame, textvariable=self.contact_var)
        self.contact_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Address
        ttk.Label(self.form_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5)
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(self.form_frame, textvariable=self.address_var)
        self.address_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Phone
        ttk.Label(self.form_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(self.form_frame, textvariable=self.phone_var)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Email
        ttk.Label(self.form_frame, text="Email:").grid(row=2, column=2, padx=5, pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self.form_frame, textvariable=self.email_var)
        self.email_entry.grid(row=2, column=3, padx=5, pady=5)
        
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
    
    def refresh(self, suppliers=None):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        if suppliers:
            for supplier in suppliers:
                self.tree.insert(
                    "", 
                    tk.END, 
                    values=(
                        supplier["supplier_id"],
                        supplier["name"],
                        supplier["contact_name"],
                        supplier["address"],
                        supplier["phone"],
                        supplier["email"]
                    )
                )
    
    def _on_add(self):
        if self.controller:
            self.controller.add_supplier(
                self.name_var.get(),
                self.contact_var.get(),
                self.address_var.get(),
                self.phone_var.get(),
                self.email_var.get()
            )
    
    def _on_update(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error("Please select a supplier to update")
            return
            
        if self.controller:
            supplier_id = self.tree.item(selected[0])["values"][0]
            self.controller.update_supplier(
                supplier_id,
                self.name_var.get(),
                self.contact_var.get(),
                self.address_var.get(),
                self.phone_var.get(),
                self.email_var.get()
            )
    
    def _on_delete(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error("Please select a supplier to delete")
            return
            
        if self.controller:
            supplier_id = self.tree.item(selected[0])["values"][0]
            self.controller.delete_supplier(supplier_id)
    
    def _on_clear(self):
        """Clear all form fields"""
        self.name_var.set("")
        self.contact_var.set("")
        self.address_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        
        # Deselect tree item
        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)
    
    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.name_var.set(values[1])
            self.contact_var.set(values[2])
            self.address_var.set(values[3])
            self.phone_var.set(values[4])
            self.email_var.set(values[5])
