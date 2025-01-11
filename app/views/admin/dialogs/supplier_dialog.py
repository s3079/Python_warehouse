import customtkinter as ctk
from datetime import datetime

class SupplierDialog(ctk.CTkToplevel):
    def __init__(self, parent, supplier=None, on_save=None):
        super().__init__(parent)
        
        # Set up the dialog window
        self.title("Add Supplier" if not supplier else "Edit Supplier")
        self.geometry("500x600")  
        self.resizable(False, False)
        
        # Store callback and supplier
        self.on_save = on_save
        self.supplier = supplier
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Create main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Add header
        header_text = "Add New Supplier" if not supplier else "Edit Supplier"
        header = ctk.CTkLabel(
            main_container,
            text=header_text,
            font=("", 20, "bold"),
            text_color="#16151C"
        )
        header.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # Name field
        name_label = ctk.CTkLabel(
            main_container,
            text="Name",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        name_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Enter supplier name",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # Contact Name field
        contact_name_label = ctk.CTkLabel(
            main_container,
            text="Contact Name",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        contact_name_label.grid(row=3, column=0, sticky="w", pady=(0, 5))
        
        self.contact_name_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Enter contact name",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.contact_name_entry.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        
        # Email field
        email_label = ctk.CTkLabel(
            main_container,
            text="Email",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        email_label.grid(row=5, column=0, sticky="w", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Enter email address",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.email_entry.grid(row=6, column=0, sticky="ew", pady=(0, 15))
        
        # Phone field
        phone_label = ctk.CTkLabel(
            main_container,
            text="Phone",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        phone_label.grid(row=7, column=0, sticky="w", pady=(0, 5))
        
        self.phone_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Enter phone number",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.phone_entry.grid(row=8, column=0, sticky="ew", pady=(0, 15))
        
        # Address field
        address_label = ctk.CTkLabel(
            main_container,
            text="Address",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        address_label.grid(row=9, column=0, sticky="w", pady=(0, 5))
        
        self.address_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Enter address",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.address_entry.grid(row=10, column=0, sticky="ew", pady=(0, 20))
        
        # Add buttons container
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.grid(row=11, column=0, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            height=45,
            corner_radius=8,
            command=self.destroy
        )
        cancel_button.grid(row=0, column=0, sticky="e", padx=(0, 10))
        
        # Save button
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Save Supplier",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            height=45,
            corner_radius=8,
            command=self.save_supplier
        )
        save_button.grid(row=0, column=1, sticky="e")
        
        # If editing, populate fields with existing data
        if supplier:
            self.name_entry.insert(0, supplier.get("name", ""))
            self.contact_name_entry.insert(0, supplier.get("contact_name", ""))
            self.email_entry.insert(0, supplier.get("email", ""))
            self.phone_entry.insert(0, supplier.get("phone", ""))
            self.address_entry.insert(0, supplier.get("address", ""))
        
        # Focus on name entry
        self.name_entry.focus_set()
    
    def save_supplier(self):
        """Validate and save supplier data"""
        name = self.name_entry.get().strip()
        contact_name = self.contact_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        
        # Validate name
        if not name:
            self.show_error("Name is required")
            return
        
        # Prepare supplier data
        supplier_data = {
            "name": name,
            "contact_name": contact_name,
            "email": email,
            "phone": phone,
            "address": address,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        }
        
        # If editing, include supplier_id
        if self.supplier:
            supplier_data["supplier_id"] = self.supplier.get("supplier_id")
        
        # Call save callback
        if self.on_save:
            try:
                self.on_save(supplier_data)
                self.destroy()
            except Exception as e:
                self.show_error(str(e))
    
    def show_error(self, message):
        """Show error message in a dialog"""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x150")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        # Center the error dialog
        error_dialog.grid_columnconfigure(0, weight=1)
        error_dialog.grid_rowconfigure(0, weight=1)
        
        # Add error message
        message_label = ctk.CTkLabel(
            error_dialog,
            text=message,
            font=("", 13),
            text_color="#FF4842",
            wraplength=250
        )
        message_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Add OK button
        ok_button = ctk.CTkButton(
            error_dialog,
            text="OK",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            height=35,
            corner_radius=8,
            command=error_dialog.destroy
        )
        ok_button.grid(row=1, column=0, pady=(0, 20))