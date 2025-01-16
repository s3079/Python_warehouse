import customtkinter as ctk
from app.views.admin.dialogs.center_dialog import CenterDialog

class OrderDialog(CenterDialog):
    def __init__(self, parent, order=None, on_save=None):
        title = "Edit Order" if order else "Add Order"
        super().__init__(parent, title, "500x700")
        
        self.order = order
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
        # Customer Name field
        customer_label = ctk.CTkLabel(
            content_frame,
            text="Customer Name*",
            font=("", 13),
            text_color="#16151C"
        )
        customer_label.pack(anchor="w")
        
        self.customer_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter customer name",
            height=40,
            width=460
        )
        self.customer_entry.pack(pady=(5, 15))
        
        # Order Date field
        date_label = ctk.CTkLabel(
            content_frame,
            text="Order Date*",
            font=("", 13),
            text_color="#16151C"
        )
        date_label.pack(anchor="w")
        
        self.date_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter order date",
            height=40,
            width=460
        )
        self.date_entry.pack(pady=(5, 15))
        
        # Total Amount field
        total_label = ctk.CTkLabel(
            content_frame,
            text="Total Amount*",
            font=("", 13),
            text_color="#16151C"
        )
        total_label.pack(anchor="w")
        
        self.total_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter total amount",
            height=40,
            width=460
        )
        self.total_entry.pack(pady=(5, 15))
        
        # Status field
        status_label = ctk.CTkLabel(
            content_frame,
            text="Status*",
            font=("", 13),
            text_color="#16151C"
        )
        status_label.pack(anchor="w")
        
        self.status_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter order status",
            height=40,
            width=460
        )
        self.status_entry.pack(pady=(5, 15))
        
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
            command=self.save_order
        )
        save_button.pack(side="left")
        
        # If editing, populate fields with existing data
        if order:
            self.customer_entry.insert(0, order["customer_name"])
            self.date_entry.insert(0, order["order_date"])
            self.total_entry.insert(0, str(order["total_amount"]))
            self.status_entry.insert(0, order["status"])
    
    def save_order(self):
        """Validate and save order data"""
        try:
            # Get values from form
            customer_name = self.customer_entry.get().strip()
            order_date = self.date_entry.get().strip()
            total_amount = self.total_entry.get().strip()
            status = self.status_entry.get().strip()
            
            # Validate required fields
            if not customer_name:
                raise ValueError("Customer name is required")
            if not order_date:
                raise ValueError("Order date is required")
            if not status:
                raise ValueError("Status is required")
            
            # Validate total amount format
            try:
                total_amount = float(total_amount)
                if total_amount < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Total amount must be a positive number")
            
            # Prepare data for saving
            data = {
                "customer_name": customer_name,
                "order_date": order_date,
                "total_amount": total_amount,
                "status": status
            }
            
            # If editing, include order_id
            if self.order:
                data["order_id"] = self.order["order_id"]
            
            # Call save callback
            if self.on_save:
                self.on_save(data)
            
            # Close dialog
            self.destroy()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e)) 