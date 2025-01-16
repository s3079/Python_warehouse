import customtkinter as ctk
import tkinter as tk
from app.views.admin.dialogs.center_dialog import CenterDialog

class FilterDialog(CenterDialog):
    def __init__(self, parent, on_apply=None):
        super().__init__(parent, "Lọc sản phẩm", "400x300")
        
        self.on_apply = on_apply
        
        # Store filter states
        self.name_sort = tk.StringVar(value="none")  # none, asc, desc
        self.price_sort = tk.StringVar(value="none")  # none, asc, desc
        
        # Create main content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Name filter section
        name_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Tên sản phẩm",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        name_label.pack(anchor="w", pady=(0, 10))
        
        # Name radio buttons
        name_options_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        name_options_frame.pack(fill="x")
        
        name_all = ctk.CTkRadioButton(
            name_options_frame,
            text="Tất cả",
            variable=self.name_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        name_all.pack(side="left", padx=(0, 15))
        
        name_asc = ctk.CTkRadioButton(
            name_options_frame,
            text="A-Z",
            variable=self.name_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        name_asc.pack(side="left", padx=(0, 15))
        
        name_desc = ctk.CTkRadioButton(
            name_options_frame,
            text="Z-A",
            variable=self.name_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        name_desc.pack(side="left")
        
        # Price filter section
        price_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=(0, 20))
        
        price_label = ctk.CTkLabel(
            price_frame,
            text="Giá",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        price_label.pack(anchor="w", pady=(0, 10))
        
        # Price radio buttons
        price_options_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        price_options_frame.pack(fill="x")
        
        price_all = ctk.CTkRadioButton(
            price_options_frame,
            text="Tất cả",
            variable=self.price_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        price_all.pack(side="left", padx=(0, 15))
        
        price_asc = ctk.CTkRadioButton(
            price_options_frame,
            text="Thấp đến cao",
            variable=self.price_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        price_asc.pack(side="left", padx=(0, 15))
        
        price_desc = ctk.CTkRadioButton(
            price_options_frame,
            text="Cao đến thấp",
            variable=self.price_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        price_desc.pack(side="left")
        
        # Add buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
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
        
        # Apply button
        apply_button = ctk.CTkButton(
            buttons_frame,
            text="Áp dụng",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=self.apply_filters
        )
        apply_button.pack(side="left")

    def apply_filters(self):
        """Get filter values and call the callback"""
        if self.on_apply:
            filters = {
                "name_sort": self.name_sort.get(),
                "price_sort": self.price_sort.get()
            }
            self.on_apply(filters)
        self.destroy() 