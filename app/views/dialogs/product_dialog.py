import customtkinter as ctk
from app.views.dialogs.center_dialog import CenterDialog

class ProductDialog(CenterDialog):
    def __init__(self, parent, product=None, on_save=None):
        title = "Sửa Sản Phẩm" if product else "Thêm Sản Phẩm"
        super().__init__(parent, title, "500x700")
        
        self.product = product
        self.on_save = on_save
        
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        heading_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=("", 16, "bold"),
            text_color="#16151C"
        )
        heading_label.pack(pady=(0, 20))
        
        name_label = ctk.CTkLabel(
            content_frame,
            text="Tên*",
            font=("", 13),
            text_color="#16151C"
        )
        name_label.pack(anchor="w")
        
        self.name_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Nhập tên sản phẩm",
            height=40,
            width=460
        )
        self.name_entry.pack(pady=(5, 15))
        
        desc_label = ctk.CTkLabel(
            content_frame,
            text="Mô tả",
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
        
        price_label = ctk.CTkLabel(
            content_frame,
            text="Đơn giá (VND)*",
            font=("", 13),
            text_color="#16151C"
        )
        price_label.pack(anchor="w")
        
        self.price_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Nhập đơn giá",
            height=40,
            width=460
        )
        self.price_entry.pack(pady=(5, 15))
        
        category_label = ctk.CTkLabel(
            content_frame,
            text="Danh mục*",
            font=("", 13),
            text_color="#16151C"
        )
        category_label.pack(anchor="w")
        
        self.category_var = ctk.StringVar()
        self.category_dropdown = ctk.CTkOptionMenu(
            content_frame,
            variable=self.category_var,
            values=self.lay_danh_muc(),
            width=460,
            height=40,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        self.category_dropdown.pack(pady=(5, 15))
        
        supplier_label = ctk.CTkLabel(
            content_frame,
            text="Nhà cung cấp*",
            font=("", 13),
            text_color="#16151C"
        )
        supplier_label.pack(anchor="w")
        
        self.supplier_var = ctk.StringVar()
        self.supplier_dropdown = ctk.CTkOptionMenu(
            content_frame,
            variable=self.supplier_var,
            values=self.lay_nha_cung_cap(),
            width=460,
            height=40,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA"
        )
        self.supplier_dropdown.pack(pady=(5, 15))
        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        buttons_container = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        buttons_container.pack(side="right")
        
        cancel_button = ctk.CTkButton(
            buttons_container,
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
        
        save_button = ctk.CTkButton(
            buttons_container,
            text='Lưu',
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=self.luu_san_pham
        )
        save_button.pack(side="left")
        
        if product:
            self.name_entry.insert(0, product["ten"])
            if product["mo_ta"]:
                self.desc_entry.insert("1.0", product["mo_ta"])
            self.price_entry.insert(0, f"{int(product['don_gia']):,}")
            from app.controllers.category_controller import CategoryController
            from app.controllers.supplier_controller import SupplierController
            category_controller = CategoryController()
            supplier_controller = SupplierController()
            category_data = category_controller.lay_danh_muc_theo_id(product["ma_danh_muc"])
            supplier_data = supplier_controller.lay_nha_cung_cap_theo_id(product["ma_ncc"])
            self.category_var.set(category_data["ten"])
            self.supplier_var.set(supplier_data["ten"])
    
    def lay_danh_muc(self):
        from app.controllers.category_controller import CategoryController
        controller = CategoryController()
        categories = controller.layTatCaDanhMuc()
        return [category["ten"] for category in categories] if categories else []
    
    def lay_nha_cung_cap(self):
        from app.controllers.supplier_controller import SupplierController
        controller = SupplierController()
        suppliers = controller.layTatCaNhaCungCap()
        return [supplier["ten"] for supplier in suppliers] if suppliers else []
    
    def luu_san_pham(self):
        try:
            ten = self.name_entry.get().strip()
            mo_ta = self.desc_entry.get("1.0", "end-1c").strip()
            don_gia = self.price_entry.get().strip().replace(',', '')
            category = self.category_var.get()
            supplier = self.supplier_var.get()
            
            if not ten:
                raise ValueError("Tên sản phẩm là bắt buộc")
            if not don_gia:
                raise ValueError("Đơn giá là bắt buộc")
            if not category:
                raise ValueError("Danh mục là bắt buộc")
            if not supplier:
                raise ValueError("Nhà cung cấp là bắt buộc")
            
            try:
                don_gia = float(don_gia)
                if don_gia < 0:
                    raise ValueError
                if don_gia > 999999999:
                    raise ValueError("Đơn giá không được vượt quá 999,999,999 VND")
                don_gia = round(don_gia)
            except ValueError as e:
                if "không được vượt quá" in str(e):
                    raise e
                raise ValueError("Đơn giá phải là số dương")
            
            category_data = self.lay_danh_muc_theo_ten(category)
            supplier_data = self.lay_nha_cung_cap_theo_ten(supplier)
            
            if not category_data or not supplier_data:
                raise ValueError("Danh mục hoặc nhà cung cấp không hợp lệ")

            data = {
                "ten": ten,
                "mo_ta": mo_ta,
                "don_gia": don_gia,
                "ma_danh_muc": category_data["ma_danh_muc"],
                "ma_ncc": supplier_data["ma_ncc"]
            }
            
            if self.product:
                data["ma_san_pham"] = self.product["ma_san_pham"]
            
            if self.on_save:
                self.on_save(data)
            
            self.destroy()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e))

    def lay_danh_muc_theo_ten(self, category_name):
        from app.controllers.category_controller import CategoryController
        controller = CategoryController()
        categories = controller.layTatCaDanhMuc()
        return next((cat for cat in categories if cat["ten"] == category_name), None)

    def lay_nha_cung_cap_theo_ten(self, supplier_name):
        from app.controllers.supplier_controller import SupplierController
        controller = SupplierController()
        suppliers = controller.layTatCaNhaCungCap()
        return next((sup for sup in suppliers if sup["ten"] == supplier_name), None)