import customtkinter as ctk
from PIL import Image
from pathlib import Path
from app.controllers.category_controller import CategoryController
from app.views.dialogs.category_dialog import CategoryDialog
from app.views.dialogs.center_dialog import CenterDialog
import math
import tkinter as tk

class CategoriesPage(ctk.CTkFrame):
    def __init__(self, parent, controller, can_edit=True):
        super().__init__(parent, fg_color="transparent")
        self.controller = CategoryController()
        self.can_edit = can_edit
        self.trang_hien_tai = 1
        self.so_muc_moi_trang = 10
        self.tong_so_muc = 0
        self.tu_khoa_tim = ""
        

        assets_path = Path(__file__).parent.parent.parent/ 'app' / 'assets' / 'icons'
        self.search_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'search.png')),
            size=(20, 20)
        )
        self.filter_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'filter.png')),
            size=(20, 20)
        )
        self.plus_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'plus.png')),
            size=(20, 20)
        )
        self.trash_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'trash.png')),
            size=(16, 16)
        )
        self.edit_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'edit.png')),
            size=(16, 16)
        )
        self.chevron_left_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-left.png')),
            size=(20, 20)
        )
        self.chevron_right_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-right.png')),
            size=(20, 20)
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        top_section = ctk.CTkFrame(self, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 20))
        top_section.grid_columnconfigure(1, weight=1)
        
        search_frame = ctk.CTkFrame(
            top_section,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        search_frame.grid(row=0, column=0, sticky="w")
        
        search_icon_label = ctk.CTkLabel(
            search_frame,
            text="",
            image=self.search_icon
        )
        search_icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm kiếm danh mục...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        self.search_entry.bind("<Return>", self.khi_tim_kiem)
        
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        filter_button = ctk.CTkButton(
            buttons_frame,
            text="Lọc",
            image=self.filter_icon,
            compound="left",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=45,
            corner_radius=8,
            command=self.hien_thi_bo_loc
        )
        filter_button.pack(side="left", padx=(0, 10))
        
        new_category_button = ctk.CTkButton(
            buttons_frame,
            text="Thêm Danh Mục",
            image=self.plus_icon,
            compound="left",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=140,
            height=45,
            corner_radius=8,
            command=self.hien_thi_them_moi
        )
        new_category_button.pack(side="left")
        
        table_container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        table_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        self.table_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent"
        )
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        self.columns = [
            {"name": "Tên danh mục", "key": "ten", "width": 200},
            {"name": "Mô tả", "key": "mo_ta", "width": 300},
            {"name": "Tổng sản phẩm", "key": "tong_san_pham", "width": 120},
            {"name": "Thao tác", "key": "actions", "width": 80}
        ]
        
        header_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="#F8F9FA",
            height=50
        )
        header_frame.pack(fill="x", expand=True)
        header_frame.pack_propagate(False)
        
        for i, col in enumerate(self.columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col["name"],
                font=("", 13, "bold"),
                text_color="#16151C",
                anchor="w",
                width=col["width"]
            )
            label.grid(row=0, column=i, padx=(20 if i == 0 else 10, 10), pady=15, sticky="w")
            
        self.content_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True)
        
        self.tai_danh_muc()
    
    def khi_tim_kiem(self, event=None):
        self.tu_khoa_tim = self.search_entry.get().strip()
        self.trang_hien_tai = 1
        self.tai_danh_muc()

    def tai_danh_muc(self):
        """Load categories with current filters"""
        try:
            categories = self.controller.layTatCaDanhMuc(
                name_sort=self.name_sort_value if hasattr(self, 'name_sort_value') else "none",
                desc_sort=self.desc_sort_value if hasattr(self, 'desc_sort_value') else "none",
                ten_filter=self.tu_khoa_tim
            )
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            offset = (self.trang_hien_tai - 1) * self.so_muc_moi_trang
            
            self.tong_so_muc = len(categories)
            start_idx = offset
            end_idx = start_idx + self.so_muc_moi_trang
            categories = categories[start_idx:end_idx]

            self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)
            
            for i, category in enumerate(categories):
                row_frame = ctk.CTkFrame(
                    self.content_frame,
                    fg_color="white" if i % 2 == 0 else "#F8F9FA",
                    height=50
                )
                row_frame.pack(fill="x")
                
                for j, col in enumerate(self.columns):
                    if col["key"] == "actions":
                        actions_frame = ctk.CTkFrame(
                            row_frame,
                            fg_color="transparent"
                        )
                        actions_frame.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                        
                        edit_btn = ctk.CTkButton(
                            actions_frame,
                            text="",
                            image=self.edit_icon,
                            width=30,
                            height=30,
                            fg_color="#006EC4",
                            text_color="white",
                            hover_color="#0059A1",
                            command=lambda c=category: self.hien_thi_chinh_sua(c)
                        )
                        edit_btn.pack(side="left", padx=(0, 5))
                        
                        delete_btn = ctk.CTkButton(
                            actions_frame,
                            text="",
                            image=self.trash_icon,
                            width=30,
                            height=30,
                            fg_color="#e03137",
                            text_color="white",
                            hover_color="#b32429",
                            command=lambda c=category: self.xoa_danh_muc(c)
                        )
                        delete_btn.pack(side="left")
                        
                    else:
                        value = str(category.get(col["key"], "") or "")
                        label = ctk.CTkLabel(
                            row_frame,
                            text=value,
                            anchor="w",
                            width=col["width"]
                        )
                        label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                
                separator = ctk.CTkFrame(
                    self.content_frame,
                    fg_color="#E5E5E5",
                    height=1
                )
                separator.pack(fill="x")
    
            self.tao_dieu_khien_phan_trang()
        except Exception as e:
            print(f"Error loading categories: {e}")

    def tao_dieu_khien_phan_trang(self):
        if hasattr(self, 'pagination_frame'):
            for widget in self.pagination_frame.winfo_children():
                widget.destroy()
        else:
            self.pagination_frame = ctk.CTkFrame(self, fg_color="white", height=60)
            self.pagination_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
            self.pagination_frame.grid_propagate(False)
        
        controls_frame = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        controls_frame.pack(expand=True, fill="both")
        
        left_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=20)
        
        start_index = (self.trang_hien_tai - 1) * self.so_muc_moi_trang + 1
        end_index = min(start_index + self.so_muc_moi_trang - 1, self.tong_so_muc)
        
        showing_label = ctk.CTkLabel(
            left_frame,
            text=f"Hiển thị {start_index}-{end_index} trong {self.tong_so_muc} danh mục",
            text_color="#6F6E77"
        )
        showing_label.pack(side="left")
        
        right_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=20)
        
        prev_button = ctk.CTkButton(
            right_frame,
            text="",
            image=self.chevron_left_image,
            width=30,
            height=30,
            fg_color="#F8F9FA" if self.trang_hien_tai > 1 else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.trang_truoc if self.trang_hien_tai > 1 else None
        )
        prev_button.pack(side="left", padx=(0, 5))
        
        total_pages = math.ceil(self.tong_so_muc / self.so_muc_moi_trang)
        visible_pages = 5
        start_page = max(1, min(self.trang_hien_tai - visible_pages // 2,
                               total_pages - visible_pages + 1))
        end_page = min(start_page + visible_pages - 1, total_pages)
        
        for page in range(start_page, end_page + 1):
            is_current = page == self.trang_hien_tai
            page_button = ctk.CTkButton(
                right_frame,
                text=str(page),
                width=30,
                height=30,
                fg_color="#006EC4" if is_current else "#F8F9FA",
                text_color="white" if is_current else "#16151C",
                hover_color="#0059A1" if is_current else "#E8E9EA",
                command=lambda p=page: self.den_trang(p)
            )
            page_button.pack(side="left", padx=2)
        
        next_button = ctk.CTkButton(
            right_frame,
            text="",
            image=self.chevron_right_image,
            width=30,
            height=30,
            fg_color="#F8F9FA" if self.trang_hien_tai < total_pages else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.trang_sau if self.trang_hien_tai < total_pages else None
        )
        next_button.pack(side="left", padx=(5, 0))

    def trang_truoc(self):
        if self.trang_hien_tai > 1:
            self.trang_hien_tai -= 1
            self.tai_danh_muc()

    def trang_sau(self):
        self.trang_hien_tai += 1
        self.tai_danh_muc()

    def den_trang(self, trang):
        self.trang_hien_tai = trang
        self.tai_danh_muc()

    def hien_thi_them_moi(self):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = CategoryDialog(
            self,
            on_save=self.luu_danh_muc
        )

    def hien_thi_chinh_sua(self, danh_muc):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = CategoryDialog(
            self,
            category=danh_muc,
            on_save=self.luu_danh_muc
        )

    def xoa_danh_muc(self, danh_muc):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = CenterDialog(self, "Xoá Danh Mục")
        
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        warning_label = ctk.CTkLabel(
            content_frame,
            text="⚠️ Cảnh Báo",
            font=("", 16, "bold"),
            text_color="#e03137"
        )
        warning_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(
            content_frame,
            text=f"Bạn có chắc chắn muốn xóa '{danh_muc['ten']}' không?\nKhông thể hoàn tác hành động này.",
            font=("", 13),
            text_color="#16151C"
        )
        message_label.pack(pady=(0, 20))
        
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
        button_container = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        button_container.pack(side="right")
        button_containerCancel = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        button_containerCancel.pack(side="left")

        cancel_button = ctk.CTkButton(
            button_containerCancel,
            text="Hủy",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        

        delete_button = ctk.CTkButton(
            button_container,
            text="Xóa",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.xac_nhan_xoa(dialog, danh_muc)
        )
        delete_button.pack(side="left")

    def xac_nhan_xoa(self, dialog, danh_muc):
        try:
            self.controller.xoa(danh_muc["ma_danh_muc"])
            dialog.destroy()
            self.tai_danh_muc()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", f"Không thể xóa danh mục: {str(e)}")

    def luu_danh_muc(self, du_lieu_danh_muc):
        try:
            if "ma_danh_muc" in du_lieu_danh_muc:
                self.controller.capNhat(
                    du_lieu_danh_muc["ma_danh_muc"],
                    du_lieu_danh_muc["ten"],
                    du_lieu_danh_muc["mo_ta"]
                )
            else:
                self.controller.them(
                    du_lieu_danh_muc["ten"],
                    du_lieu_danh_muc["mo_ta"]
                )
            self.tai_danh_muc()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", f"Không thể lưu danh mục: {str(e)}")

    def hien_thi_bo_loc(self):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = CenterDialog(self, "Lọc danh muc", "400x300")

        self.name_sort = tk.StringVar(value="none")
        self.desc_sort = tk.StringVar(value="none")
        
      
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
    
        name_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Tên Danh Mục",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        name_label.pack(anchor="w", pady=(0, 10))
        
     
        name_options_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        name_options_frame.pack(fill="x")
        
        name_all = ctk.CTkRadioButton(
            name_options_frame,
            text="Tất Cả",
            variable=self.name_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        name_all.pack(side="left", padx=(0, 15))
        
        name_asc = ctk.CTkRadioButton(
            name_options_frame,
            text="Từ A-Z",
            variable=self.name_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        name_asc.pack(side="left", padx=(0, 15))
        
        name_desc = ctk.CTkRadioButton(
            name_options_frame,
            text="Từ Z-A",
            variable=self.name_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        name_desc.pack(side="left")
        
       
        desc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        desc_frame.pack(fill="x", pady=(0, 20))
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Mô Tả",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        desc_label.pack(anchor="w", pady=(0, 10))
        
       
        desc_options_frame = ctk.CTkFrame(desc_frame, fg_color="transparent")
        desc_options_frame.pack(fill="x")
        
        desc_all = ctk.CTkRadioButton(
            desc_options_frame,
            text="Tất Cả",
            variable=self.desc_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        desc_all.pack(side="left", padx=(0, 15))
        
        desc_asc = ctk.CTkRadioButton(
            desc_options_frame,
            text="Từ A-Z",
            variable=self.desc_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        desc_asc.pack(side="left", padx=(0, 15))
        
        desc_desc = ctk.CTkRadioButton(
            desc_options_frame,
            text="Từ Z-A",
            variable=self.desc_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        desc_desc.pack(side="left")
        
        
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
     
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Hủy",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        apply_button = ctk.CTkButton(
            buttons_frame,
            text="Áp Dụng",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.ap_dung_bo_loc(dialog)
        )
        apply_button.pack(side="left")

    def ap_dung_bo_loc(self, dialog):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog.destroy()
        self.trang_hien_tai = 1
        self.name_sort_value = self.name_sort.get()
        self.desc_sort_value = self.desc_sort.get()
        self.tai_danh_muc()
