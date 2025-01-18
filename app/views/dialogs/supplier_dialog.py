import customtkinter as ctk

class SupplierDialog(ctk.CTkToplevel):
    def __init__(self, parent, supplier=None, on_save=None):
        super().__init__(parent)
        
        self.title("Thêm Nhà Cung Cấp" if not supplier else "Sửa Nhà Cung Cấp")
        self.geometry("500x600")  
        self.resizable(False, False)
        
        self.on_save = on_save
        self.supplier = supplier
        
        self.transient(parent)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        
        header_text = "Thêm Nhà Cung Cấp" if not supplier else "Sửa Nhà Cung Cấp"
        header = ctk.CTkLabel(
            main_container,
            text=header_text,
            font=("", 20, "bold"),
            text_color="#16151C"
        )
        header.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        name_label = ctk.CTkLabel(
            main_container,
            text="Tên",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        name_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Nhập tên nhà cung cấp",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        email_label = ctk.CTkLabel(
            main_container,
            text="Email",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        email_label.grid(row=5, column=0, sticky="w", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Nhập email",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.email_entry.grid(row=6, column=0, sticky="ew", pady=(0, 15))
        
        phone_label = ctk.CTkLabel(
            main_container,
            text="Số Điện Thoại",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        phone_label.grid(row=7, column=0, sticky="w", pady=(0, 5))
        
        self.phone_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Nhập số điện thoại",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.phone_entry.grid(row=8, column=0, sticky="ew", pady=(0, 15))
        
        address_label = ctk.CTkLabel(
            main_container,
            text="Địa chỉ",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        address_label.grid(row=9, column=0, sticky="w", pady=(0, 5))
        
        self.address_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Nhập địa chỉ",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.address_entry.grid(row=10, column=0, sticky="ew", pady=(0, 20))
        
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.grid(row=11, column=0, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Hủy",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            height=45,
            corner_radius=8,
            command=self.destroy
        )
        cancel_button.grid(row=0, column=0, sticky="e", padx=(0, 10))
        
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Lưu",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            height=45,
            corner_radius=8,
            command=self.luu_nha_cung_cap
        )
        save_button.grid(row=0, column=1, sticky="e")
        
        if supplier:
            self.name_entry.insert(0, supplier.get("ten", ""))
            self.email_entry.insert(0, supplier.get("email", ""))
            self.phone_entry.insert(0, supplier.get("dien_thoai", ""))
            self.address_entry.insert(0, supplier.get("dia_chi", ""))
        
        self.name_entry.focus_set()
    
    def luu_nha_cung_cap(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name:
            self.hien_thi_loi("Tên là bắt buộc")
            return
        
        supplier_data = {
            "ten": name,
            "dia_chi": address,
            "dien_thoai": phone,
            "email": email,
        }
        
        if self.supplier:
            supplier_data["ma_ncc"] = self.supplier.get("ma_ncc")
        
        if self.on_save:
            try:
                self.on_save(supplier_data)
                self.destroy()
            except Exception as e:
                self.hien_thi_loi(str(e))
    
    def hien_thi_loi(self, message):
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Lỗi")
        error_dialog.geometry("300x150")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        error_dialog.grid_columnconfigure(0, weight=1)
        error_dialog.grid_rowconfigure(0, weight=1)
        
        message_label = ctk.CTkLabel(
            error_dialog,
            text=message,
            font=("", 13),
            text_color="#FF4842",
            wraplength=250
        )
        message_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
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