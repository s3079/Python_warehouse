import customtkinter as ctk
from tkcalendar import DateEntry
from app.views.admin.dialogs.center_dialog import CenterDialog

class InventoryDialog(CenterDialog):
    def __init__(self, parent, inventory=None, on_save=None):
        title = "Edit Inventory" if inventory else "Add Inventory"
        super().__init__(parent, title, "400x450")
        
        self.inventory = inventory
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
        
        # Product selection
        product_label = ctk.CTkLabel(
            content_frame,
            text="Product*",
            font=("", 13),
            text_color="#16151C"
        )
        product_label.pack(anchor="w")
        
        self.selected_product = ctk.StringVar()
        self.product_map = self.get_product_map()
        product_names = list(self.product_map.keys())
        
        self.product_dropdown = ctk.CTkOptionMenu(
            content_frame,
            variable=self.selected_product,
            values=product_names,
            width=460,
            height=40,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        self.product_dropdown.pack(pady=(5, 15))
        
        # Quantity entry
        quantity_label = ctk.CTkLabel(
            content_frame,
            text="Quantity*",
            font=("", 13),
            text_color="#16151C"
        )
        quantity_label.pack(anchor="w")
        
        self.quantity_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter Quantity",
            height=40,
            width=460
        )
        self.quantity_entry.pack(pady=(5, 15))
        
        # Last restock date entry (optional)
        restock_date_label = ctk.CTkLabel(
            content_frame,
            text="Last Restock Date",
            font=("", 13),
            text_color="#16151C"
        )
        restock_date_label.pack(anchor="w")
        
        self.restock_date_entry = DateEntry(
            content_frame,
            width=42,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='y-mm-dd'
        )
        self.restock_date_entry.pack(pady=(5, 15))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
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
            buttons_frame,
            text="Save",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=self.save_inventory
        )
        save_button.pack(side="left")
        
        # If editing, populate fields with existing data
        if inventory:
            self.selected_product.set(inventory["product_name"])
            self.quantity_entry.insert(0, str(inventory["quantity"]))
            if inventory.get("last_restock_date"):
                self.restock_date_entry.set_date(inventory["last_restock_date"])
    
    def get_product_map(self):
        """Get a map of product names to product IDs"""
        from app.controllers.product_controller import ProductController
        controller = ProductController()
        products = controller.get_all_products()
        return {product["name"]: product["product_id"] for product in products} if products else {}
    
    def save_inventory(self):
        """Validate and save inventory data"""
        try:
            # Get values from form
            product_name = self.selected_product.get()
            quantity = self.quantity_entry.get().strip()
            restock_date = self.restock_date_entry.get_date()
            
            # Validate required fields
            if not product_name:
                raise ValueError("Product is required")
            if not quantity.isdigit():
                raise ValueError("Quantity must be a positive integer")
            
            # Retrieve product ID from the map
            product_id = self.product_map.get(product_name)
            if product_id is None:
                raise ValueError("Invalid product selected")
            
            # Prepare data for saving
            data = {
                "product_id": product_id,
                "quantity": int(quantity),
                "last_restock_date": restock_date
            }
            
            # If editing, include inventory_id
            if self.inventory:
                data["inventory_id"] = self.inventory["inventory_id"]
            
            # Call save callback
            if self.on_save:
                self.on_save(data)
            
            # Close dialog
            self.destroy()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e)) 