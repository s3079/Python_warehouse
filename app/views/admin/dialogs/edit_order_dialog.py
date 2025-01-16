import customtkinter as ctk
from app.controllers.order_controller import OrderController
from app.views.admin.dialogs.center_dialog import CenterDialog
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime

class EditOrderDialog(CenterDialog):
    def __init__(self, parent, order_data, on_save=None):
        super().__init__(parent, "Sửa đơn hàng", "500x700")
        
        # Get order details and store data
        self.order_data = order_data
        self.on_save = on_save
        self.chi_tiet_don_hang = self.lay_chi_tiet_don_hang(order_data['ma_don_hang'])
        self.san_pham = self.lay_tat_ca_san_pham()

        print("order_details:", self.chi_tiet_don_hang)  # For debugging
        print("order_data:", order_data)  # For debugging

        # Create main content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add heading with order ID
        heading_label = ctk.CTkLabel(
            content_frame,
            text=f"Sửa đơn hàng #{order_data['ma_don_hang']}",
            font=("", 16, "bold"),
            text_color="#16151C"
        )
        heading_label.pack(pady=(0, 20))

        # Order Date field with Date Picker Button
        date_label = ctk.CTkLabel(
            content_frame,
            text="Ngày đặt*",
            font=("", 13),
            text_color="#16151C"
        )
        date_label.pack(anchor="w")

        date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=(5, 15))

        # Format the order date to yyyy-mm-dd
        order_date = self.chi_tiet_don_hang.get('ngay_dat')
        if isinstance(order_date, datetime):
            formatted_date = order_date.strftime('%Y-%m-%d')
        else:
            try:
                # Try to parse the date string if it's not already a datetime
                parsed_date = datetime.strptime(str(order_date), '%Y-%m-%d')
                formatted_date = parsed_date.strftime('%Y-%m-%d')
            except:
                formatted_date = datetime.now().strftime('%Y-%m-%d')

        # Date display entry (read-only)
        self.date_var = tk.StringVar(value=formatted_date)
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
            text="📅",
            width=40,
            height=40,
            command=self.show_calendar
        )
        self.calendar_button.pack(side="left")

        # Product dropdown
        product_label = ctk.CTkLabel(
            content_frame,
            text="Sản phẩm*",
            font=("", 13),
            text_color="#16151C"
        )
        product_label.pack(anchor="w")

        # Create dictionaries for product data
        self.product_names = {}
        self.product_prices = {}
        
        # Populate the dictionaries if products exist
        if self.san_pham:
            for product in self.san_pham:
                name = str(product.get('ten', ''))  # Use product_name instead of name
                self.product_names[name] = product.get('ma_san_pham')
                self.product_prices[name] = product.get('don_gia', 0.0)

        # Set product dropdown with current product
        self.product_var = tk.StringVar(value=self.chi_tiet_don_hang.get('ten_san_pham', ''))
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
            text="Số lượng*",
            font=("", 13),
            text_color="#16151C"
        )
        quantity_label.pack(anchor="w")

        self.quantity_var = tk.StringVar(value=str(self.chi_tiet_don_hang.get('so_luong', '')))
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
            text="Đơn giá*",
            font=("", 13),
            text_color="#16151C"
        )
        unit_price_label.pack(anchor="w")

        self.unit_price_var = tk.StringVar(value=str(self.chi_tiet_don_hang.get('don_gia', '')))
        self.unit_price_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.unit_price_var,
            height=40,
            width=460,
            state="readonly"
        )
        self.unit_price_entry.pack(pady=(5, 15))

        # Total Amount field (read-only)
        total_label = ctk.CTkLabel(
            content_frame,
            text="Tổng tiền*",
            font=("", 13),
            text_color="#16151C"
        )
        total_label.pack(anchor="w")

        self.total_var = tk.StringVar(value=str(self.chi_tiet_don_hang.get('tong_tien', '')))
        self.total_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.total_var,
            height=40,
            width=460,
            state="readonly"
        )
        self.total_entry.pack(pady=(5, 15))

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

    def lay_tat_ca_san_pham(self):
        """Get all products with their IDs and prices"""
        from app.controllers.product_controller import ProductController
        controller = ProductController()
        return controller.layTatCaSanPham()
    
    def lay_chi_tiet_don_hang(self, ma_don_hang):
        """Get order details by order ID"""
        from app.controllers.order_controller import OrderController
        controller = OrderController()
        return controller.layChiTietDonHang(ma_don_hang)

    def get_product_name_by_id(self, product_id):
        """Get product name from product ID"""
        for name, pid in self.product_names.items():
            if pid == product_id:
                return name
        return "No products available"

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

    def show_calendar(self):
        """Show calendar dialog"""
        top = ctk.CTkToplevel(self)
        top.title("Select Date")
        top.geometry("300x300")
        
        # Get current date from date_var
        try:
            current_date = datetime.strptime(self.date_var.get(), '%Y-%m-%d')
        except:
            current_date = datetime.now()
        
        # Create calendar widget with light theme colors
        cal = Calendar(
            top,
            selectmode='day',
            maxdate=datetime.now(),
            date_pattern='yyyy-mm-dd',  # Ensure consistent date format
            year=current_date.year,
            month=current_date.month,
            day=current_date.day,
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
            selected_date = cal.get_date()
            # Ensure the date is in yyyy-mm-dd format
            try:
                parsed_date = datetime.strptime(selected_date, '%Y-%m-%d')
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                self.date_var.set(formatted_date)
            except:
                self.date_var.set(datetime.now().strftime('%Y-%m-%d'))
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

    def save_order(self):
        """Validate and save order data"""
        print("Saving order...")  # For debugging
        try:
            # Get values from form
            ngay_dat = self.date_var.get().strip()
            tong_tien = self.total_var.get().strip()
            ten_san_pham = self.product_var.get()
            ma_san_pham = self.product_names[ten_san_pham]
            so_luong = self.quantity_entry.get().strip()
            don_gia = self.unit_price_var.get().strip()
            
            # Validate required fields
            if not ngay_dat:
                raise ValueError("Ngày đặt là bắt buộc")
            if not tong_tien:
                raise ValueError("Tổng tiền là bắt buộc")
            if not ten_san_pham:
                raise ValueError("Sản phẩm là bắt buộc")
            if not so_luong:
                raise ValueError("Số lượng là bắt buộc")
            if not don_gia:
                raise ValueError("Đơn giá là bắt buộc")

            # Validate numeric fields
            try:
                tong_tien = float(tong_tien)
                if tong_tien < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Tổng tiền phải là số dương")

            try:
                so_luong = int(so_luong)
                if so_luong <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Số lượng phải là số nguyên dương")

            try:
                don_gia = float(don_gia)
                if don_gia < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Đơn giá phải là số dương")

            # Prepare data for saving
            data = {
                "ma_don_hang": self.order_data['ma_don_hang'],
                "ngay_dat": ngay_dat,
                "tong_tien": tong_tien,
                "ma_san_pham": ma_san_pham,
                "so_luong": so_luong,
                "don_gia": don_gia,
                "ma_nguoi_dung": self.order_data.get('ma_nguoi_dung')
            }

            print("Data:", data)  # For debugging
            
            # Call save callback
            if self.on_save:
                self.on_save(data)
            
            # Close dialog
            self.destroy()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e)) 