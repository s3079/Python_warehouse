import customtkinter as ctk
from app.views.admin.dialogs.center_dialog import CenterDialog
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime

class AddOrderDialog(CenterDialog):
    def __init__(self, parent, user_id, on_save=None):
        super().__init__(parent, "Add Order", "500x700")

        self.user_id = user_id
        self.on_save = on_save
        self.products = self.get_products()  # Get all product data

        # Create main content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add heading
        heading_label = ctk.CTkLabel(
            content_frame,
            text="Add Order",
            font=("", 16, "bold"),
            text_color="#16151C"
        )
        heading_label.pack(pady=(0, 20))

        # Order Date field with Date Picker Button
        date_label = ctk.CTkLabel(
            content_frame,
            text="Order Date*",
            font=("", 13),
            text_color="#16151C"
        )
        date_label.pack(anchor="w")

        date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=(5, 15))

        # Date display entry (read-only)
        self.date_var = tk.StringVar()
        self.date_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_var,
            width=400,
            height=40,
            state="readonly"
        )
        self.date_entry.pack(side="left", padx=(0, 10))

        # Calendar button
        self.calendar_button = ctk.CTkButton(
            date_frame,
            text="📅",  # Calendar emoji as button text
            width=40,
            height=40,
            command=self.show_calendar
        )
        self.calendar_button.pack(side="left")

        # Total Amount field (read-only)
        total_label = ctk.CTkLabel(
            content_frame,
            text="Total Amount*",
            font=("", 13),
            text_color="#16151C"
        )
        total_label.pack(anchor="w")

        self.total_var = tk.StringVar()
        self.total_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.total_var,
            height=40,
            width=460,
            state="readonly"  # Make it read-only
        )
        self.total_entry.pack(pady=(5, 15))

        # Product dropdown
        product_label = ctk.CTkLabel(
            content_frame,
            text="Product*",
            font=("", 13),
            text_color="#16151C"
        )
        product_label.pack(anchor="w")

        # Create dictionaries for product data
        self.product_names = {}
        self.product_prices = {}
        
        # Populate the dictionaries if products exist
        if self.products:
            for product in self.products:
                name = str(product.get('name', ''))  # Use product_name instead of name
                self.product_names[name] = product.get('product_id')
                self.product_prices[name] = product.get('unit_price', 0.0)

        self.product_var = tk.StringVar()
        self.product_dropdown = ctk.CTkOptionMenu(
            content_frame,
            variable=self.product_var,
            values=list(self.product_names.keys()) if self.product_names else ["No products available"],
            width=460,
            height=40,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA",
            command=self.update_unit_price
        )
        self.product_dropdown.pack(pady=(5, 15))

        # Quantity field
        quantity_label = ctk.CTkLabel(
            content_frame,
            text="Quantity*",
            font=("", 13),
            text_color="#16151C"
        )
        quantity_label.pack(anchor="w")

        self.quantity_var = tk.StringVar()
        self.quantity_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.quantity_var,
            placeholder_text="Enter quantity",
            height=40,
            width=460
        )
        self.quantity_entry.pack(pady=(5, 15))
        self.quantity_var.trace("w", self.update_total_amount)

        # Unit Price field (read-only)
        unit_price_label = ctk.CTkLabel(
            content_frame,
            text="Unit Price*",
            font=("", 13),
            text_color="#16151C"
        )
        unit_price_label.pack(anchor="w")

        self.unit_price_var = tk.StringVar()
        self.unit_price_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.unit_price_var,
            height=40,
            width=460,
            state="readonly"  # Make it read-only
        )
        self.unit_price_entry.pack(pady=(5, 15))

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

    def get_products(self):
        """Get all products with their IDs and prices"""
        from app.controllers.product_controller import ProductController
        controller = ProductController()
        return controller.get_all_products()

    def update_unit_price(self, selected_product):
        """Update unit price based on selected product"""
        if selected_product != "No products available":
            unit_price = self.product_prices.get(selected_product, 0.0)
            self.unit_price_var.set(f"{unit_price:.2f}")
            self.update_total_amount()

    def update_total_amount(self, *args):
        """Update total amount based on quantity and unit price"""
        try:
            quantity = int(self.quantity_var.get())
            unit_price = float(self.unit_price_var.get())
            total_amount = quantity * unit_price
            self.total_var.set(f"{total_amount:.2f}")
        except (ValueError, TypeError):
            self.total_var.set("0.00")

    def save_order(self):
        """Validate and save order data"""
        try:
            # Get values from form
            order_date = self.date_var.get().strip()
            total_amount = self.total_var.get().strip()
            product_name = self.product_var.get()
            product_id = self.product_names[product_name]  # Get product ID from selected name
            quantity = self.quantity_entry.get().strip()
            unit_price = self.unit_price_var.get().strip()
            
            # Validate required fields
            if not order_date:
                raise ValueError("Order date is required")
            if not total_amount:
                raise ValueError("Total amount is required")
            if not product_name:
                raise ValueError("Product is required")
            if not quantity:
                raise ValueError("Quantity is required")
            if not unit_price:
                raise ValueError("Unit price is required")
            
            # Validate numeric fields
            try:
                total_amount = float(total_amount)
                if total_amount < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Total amount must be a positive number")
            
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Quantity must be a positive integer")
            
            try:
                unit_price = float(unit_price)
                if unit_price < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Unit price must be a positive number")
            
            # Prepare data for saving
            data = {
                "order_date": order_date,
                "total_amount": total_amount,
                "product_id": product_id,  # Use product_id instead of product_name
                "quantity": quantity,
                "unit_price": unit_price,
                "user_id": self.user_id
            }
            print(data)
            
            # Call save callback
            if self.on_save:
                self.on_save(data)
            
            # Close dialog
            self.destroy()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e)) 

    def show_calendar(self):
        # Create a new top-level window
        top = ctk.CTkToplevel(self)
        top.title("Chọn ngày")
        top.geometry("300x300")
        
        # Create calendar widget with light theme colors
        cal = Calendar(
            top,
            selectmode='day',
            maxdate=datetime.now(),
            date_pattern='yyyy-mm-dd',
            # Basic colors
            background="white",
            foreground="#16151C",
            
            # Headers (day names and week numbers)
            headersbackground="#F8F9FA",
            headersforeground="#16151C",
            
            # Selected day
            selectbackground="#006EC4",
            selectforeground="white",
            
            # Normal weekdays
            normalbackground="white",
            normalforeground="#16151C",
            
            # Weekend days
            weekendbackground="white",
            weekendforeground="#16151C",
            
            # Days from other months
            othermonthforeground="gray",
            othermonthbackground="white",
            othermonthweforeground="gray",
            othermonthwebackground="white",
            
            # Disabled states
            disabledbackground="#F8F9FA",
            disabledforeground="gray",
            disabledselectbackground="#E8E9EA",
            disabledselectforeground="gray",
            disableddaybackground="#F8F9FA",
            disableddayforeground="gray",
            
            # Border
            bordercolor="#E8E9EA"
        )
        cal.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Function to get the selected date
        def grab_date():
            self.date_var.set(cal.get_date())
            top.destroy()
        
        # Add Select button
        select_button = ctk.CTkButton(
            top,
            text="Select",
            command=grab_date
        )
        select_button.pack(pady=10)
        
        # Make the dialog modal
        top.transient(self)
        top.grab_set()
        self.wait_window(top) 