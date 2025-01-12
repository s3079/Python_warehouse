import customtkinter as ctk
from app.views.admin.dialogs.center_dialog import CenterDialog

class ProductDialog(CenterDialog):
    def __init__(self, parent, product=None, on_save=None):
        title = "Edit Product" if product else "Add Product"
        super().__init__(parent, title, "500x700")
        
        self.product = product
        self.on_save = on_save
        
        # Create main content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add heading
        heading_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=("", 16, "bold"),
            text_color="#16151C"
        )
        heading_label.pack(pady=(0, 20))
        
        # Create form fields
        # Name field
        name_label = ctk.CTkLabel(
            content_frame,
            text="Name*",
            font=("", 13),
            text_color="#16151C"
        )
        name_label.pack(anchor="w")
        
        self.name_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter product name",
            height=40,
            width=460
        )
        self.name_entry.pack(pady=(5, 15))
        
        # Description field
        desc_label = ctk.CTkLabel(
            content_frame,
            text="Description",
            font=("", 13),
            text_color="#16151C"
        )
        desc_label.pack(anchor="w")
        
        self.desc_entry = ctk.CTkTextbox(
            content_frame,
            height=100,
            width=460
        )
        self.desc_entry.pack(pady=(5, 15))
        
        # Price field
        price_label = ctk.CTkLabel(
            content_frame,
            text="Price*",
            font=("", 13),
            text_color="#16151C"
        )
        price_label.pack(anchor="w")
        
        self.price_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter product price",
            height=40,
            width=460
        )
        self.price_entry.pack(pady=(5, 15))
        
        # Category dropdown
        category_label = ctk.CTkLabel(
            content_frame,
            text="Category*",
            font=("", 13),
            text_color="#16151C"
        )
        category_label.pack(anchor="w")
        
        self.category_var = ctk.StringVar()
        self.category_dropdown = ctk.CTkOptionMenu(
            content_frame,
            variable=self.category_var,
            values=self.get_categories(),
            width=460,
            height=40,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        self.category_dropdown.pack(pady=(5, 15))
        
        # Supplier dropdown
        supplier_label = ctk.CTkLabel(
            content_frame,
            text="Supplier*",
            font=("", 13),
            text_color="#16151C"
        )
        supplier_label.pack(anchor="w")
        
        self.supplier_var = ctk.StringVar()
        self.supplier_dropdown = ctk.CTkOptionMenu(
            content_frame,
            variable=self.supplier_var,
            values=self.get_suppliers(),
            width=460,
            height=40,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        self.supplier_dropdown.pack(pady=(5, 15))
        
        # Add buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Create a container for the buttons and align them to the right
        buttons_container = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        buttons_container.pack(side="right")
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_container,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=self.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Save button
        save_button = ctk.CTkButton(
            buttons_container,
            text="Save",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=self.save_product
        )
        save_button.pack(side="left")
        
        # If editing, populate fields with existing data
        if product:
            self.name_entry.insert(0, product["name"])
            if product["description"]:
                self.desc_entry.insert("1.0", product["description"])
            self.price_entry.insert(0, str(product["unit_price"]))
            self.category_var.set(product["category_name"])
            self.supplier_var.set(product["supplier_name"])
    
    def get_categories(self):
        """Get list of categories for dropdown"""
        from app.controllers.category_controller import CategoryController
        controller = CategoryController()
        categories = controller.get_all_categories()
        return [category["name"] for category in categories] if categories else []
    
    def get_suppliers(self):
        """Get list of suppliers for dropdown"""
        from app.controllers.supplier_controller import SupplierController
        controller = SupplierController()
        suppliers = controller.get_all_suppliers()
        return [supplier["name"] for supplier in suppliers] if suppliers else []
    
    def save_product(self):
        """Validate and save product data"""
        try:
            # Get values from form
            name = self.name_entry.get().strip()
            description = self.desc_entry.get("1.0", "end-1c").strip()
            price = self.price_entry.get().strip()
            category = self.category_var.get()
            supplier = self.supplier_var.get()
            
            # Validate required fields
            if not name:
                raise ValueError("Product name is required")
            if not price:
                raise ValueError("Price is required")
            if not category:
                raise ValueError("Category is required")
            if not supplier:
                raise ValueError("Supplier is required")
            
            # Validate price format
            try:
                price = float(price)
                if price < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Price must be a positive number")
            
            # Prepare data for saving
            data = {
                "name": name,
                "description": description,
                "unit_price": price,
                "category_name": category,
                "supplier_name": supplier
            }
            
            # If editing, include product_id
            if self.product:
                data["product_id"] = self.product["product_id"]
            
            # Call save callback
            if self.on_save:
                self.on_save(data)
            
            # Close dialog
            self.destroy()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e))