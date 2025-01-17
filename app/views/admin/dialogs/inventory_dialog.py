import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from app.views.admin.dialogs.center_dialog import CenterDialog

class InventoryDialog(CenterDialog):
    def __init__(self, parent, ton_kho=None, on_save=None):
        title = "Sửa tồn kho" if ton_kho else "Thêm tồn kho"
        super().__init__(parent, title, "500x700")
        
        self.ton_kho = ton_kho
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
            text="Sản phẩm*",
            font=("", 13),
            text_color="#16151C"
        )
        product_label.pack(anchor="w")
        
        self.san_pham_duoc_chon = ctk.StringVar()
        self.san_pham_map = self.lay_danh_sach_san_pham()
        ten_san_pham = list(self.san_pham_map.keys())
        
        self.san_pham_dropdown = ctk.CTkOptionMenu(
            content_frame,
            variable=self.san_pham_duoc_chon,
            values=ten_san_pham,
            width=460,
            height=40,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        self.san_pham_dropdown.pack(pady=(5, 15))
        
        # Quantity entry
        quantity_label = ctk.CTkLabel(
            content_frame,
            text="Số lượng*",
            font=("", 13),
            text_color="#16151C"
        )
        quantity_label.pack(anchor="w")
        
        self.so_luong_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Nhập số lượng",
            height=40,
            width=460
        )
        self.so_luong_entry.pack(pady=(5, 15))
        
        # Date field with Date Picker Button
        restock_date_label = ctk.CTkLabel(
            content_frame,
            text="Ngày nhập kho",
            font=("", 13),
            text_color="#16151C"
        )
        restock_date_label.pack(anchor="w")

        date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=(5, 15))

        # Date display entry (read-only)
        self.date_var = tk.StringVar()
        self.ngay_nhap_kho_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_var,
            width=400,
            height=40,
            state="readonly"
        )
        self.ngay_nhap_kho_entry.pack(side="left", padx=(0, 10))

        # Calendar button
        self.calendar_button = ctk.CTkButton(
            date_frame,
            text="📅",  # Calendar emoji as button text
            width=40,
            height=40,
            command=self.show_calendar
        )
        self.calendar_button.pack(side="left")
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Hủy",
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
            text="Lưu",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=self.luu_ton_kho
        )
        save_button.pack(side="left")
        
        # If editing, populate fields with existing data
        if ton_kho:
            self.san_pham_duoc_chon.set(ton_kho["ten_san_pham"])
            self.so_luong_entry.insert(0, str(ton_kho["so_luong"]))
            if ton_kho.get("ngay_nhap_cuoi"):
                self.date_var.set(ton_kho["ngay_nhap_cuoi"])
    
    def lay_danh_sach_san_pham(self):
        """Get a map of product names to product IDs"""
        from app.controllers.product_controller import ProductController
        controller = ProductController()
        san_pham = controller.layTatCaSanPham()
        return {sp["ten"]: sp["ma_san_pham"] for sp in san_pham} if san_pham else {}
    
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
            text="Chọn",
            command=grab_date
        )
        select_button.pack(pady=10)
        
        # Make the dialog modal
        top.transient(self)
        top.grab_set()
        self.wait_window(top)

    def luu_ton_kho(self):
        """Validate and save inventory data"""
        try:
            # Get values from form
            ten_san_pham = self.san_pham_duoc_chon.get()
            so_luong = self.so_luong_entry.get().strip()
            ngay_nhap_cuoi = self.date_var.get()  # Updated to use date_var
            
            # Validate required fields
            if not ten_san_pham:
                raise ValueError("Vui lòng chọn sản phẩm")
            if not so_luong.isdigit():
                raise ValueError("Số lượng phải là số nguyên dương")
            if not ngay_nhap_cuoi:
                raise ValueError("Vui lòng chọn ngày nhập kho")
            
            # Retrieve product ID from the map
            ma_san_pham = self.san_pham_map.get(ten_san_pham)
            if ma_san_pham is None:
                raise ValueError("Sản phẩm không hợp lệ")
            
            # Prepare data for saving
            data = {
                "ma_san_pham": ma_san_pham,
                "so_luong": int(so_luong),
                "ngay_nhap_cuoi": ngay_nhap_cuoi
            }
            
            # If editing, include inventory_id
            if self.ton_kho:
                data["ma_kho"] = self.ton_kho["ma_kho"]
            
            # Call save callback
            if self.on_save:
                self.on_save(data)
            
            # Close dialog
            self.destroy()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e)) 