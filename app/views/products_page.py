import customtkinter as ctk
from PIL import Image
from pathlib import Path
import tkinter as tk
from app.controllers.product_controller import ProductController
from app.views.dialogs.product_dialog import ProductDialog
from app.views.dialogs.center_dialog import CenterDialog
from app.views.dialogs.delete_dialog import DeleteDialog


class ProductsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, can_edit=True):
        super().__init__(parent, fg_color="transparent")
        self.controller = ProductController()
        self.can_edit = can_edit
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0
        self.search_query = ""
        
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
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
            placeholder_text="Tìm kiếm sản phẩm...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        self.search_entry.bind("<Return>", self.on_search)
        
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        filter_button = ctk.CTkButton(
            buttons_frame,
            text='Lọc',
            image=self.filter_icon,
            compound="left",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=45,
            corner_radius=8,
            command=self.show_filter_dialog
        )
        filter_button.pack(side="left", padx=(0, 10))
        
        new_product_button = ctk.CTkButton(
            buttons_frame,
            text='Thêm Sản Phẩm',
            image=self.plus_icon,
            compound="left",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=140,
            height=45,
            corner_radius=8,
            command=self.show_add_dialog
        )
        new_product_button.pack(side="left")
        
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
            {"name": "Tên sản phẩm", "key": "ten", "width": 100},
            {"name": "Mô tả", "key": "mo_ta", "width": 150},
            {"name": "Danh mục", "key": "ten_danh_muc", "width": 150},
            {"name": "Nhà cung cấp", "key": "ten_ncc", "width": 100},
            {"name": "Đơn giá", "key": "don_gia", "width": 150},
            {"name": "Thao tác", "key": "actions", "width": 100}
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
        
        self.load_products()
    
    def on_search(self, event=None):
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1
        self.load_products()

    def load_products(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Xóa nội dung bảng hiện tại
            - Tải và hiển thị danh sách sản phẩm mới
            - Định dạng hiển thị giá tiền (VD: 100,000 ₫)
            - Cắt ngắn nội dung dài và thêm tooltip
            - Tạo đường phân cách giữa các dòng
            - Cập nhật điều khiển phân trang
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        offset = (self.current_page - 1) * self.items_per_page
        
        products, total_count = self.controller.laySanPhamPhanTrang(
            offset=offset,
            limit=self.items_per_page,
            search_query=self.search_query,
            name_sort=getattr(self, 'name_sort_value', 'none'),
            price_sort=getattr(self, 'price_sort_value', 'none')
        )
        
        self.total_items = total_count
        total_pages = -(-total_count // self.items_per_page)
        
        self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)
        
        for i, product in enumerate(products):
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
                        command=lambda p=product: self.show_edit_dialog(p)
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
                        command=lambda p=product: self.delete_product(p)
                    )
                    delete_btn.pack(side="left")
                    
                elif col["key"] == "don_gia":
                    value = f"{float(product[col['key']]):,.0f} ₫"
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                else:
                    value = str(product.get(col["key"], "") or "")
                    full_text = value
                    
                    max_chars = col["width"] // 8
                    if len(value) > max_chars:
                        value = value[:max_chars-3] + "..."
                    
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                    if len(value) != len(full_text):
                        self.create_tooltip(label, full_text)
            
            separator = ctk.CTkFrame(
                self.content_frame,
                fg_color="#E5E5E5",
                height=1
            )
            separator.pack(fill="x")

        self.create_pagination_controls(total_pages)

    def create_pagination_controls(self, total_pages):
        """
        + Input:
            - total_pages: Tổng số trang
        + Output: Không có
        + Side effects:
            - Xóa điều khiển phân trang cũ nếu có
            - Tạo khung điều khiển phân trang mới
            - Hiển thị thông tin số lượng bản ghi (VD: "Hiển thị 1-10 của 50 sản phẩm")
            - Tạo nút Previous (mờ đi nếu ở trang đầu)
            - Tạo các nút số trang (tối đa 5 nút)
            - Tạo nút Next (mờ đi nếu ở trang cuối)
        """
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
        
        start_index = (self.current_page - 1) * self.items_per_page + 1
        end_index = min(start_index + self.items_per_page - 1, self.total_items)
        
        showing_label = ctk.CTkLabel(
            left_frame,
            text=f"Hiển thị {start_index}-{end_index} của {self.total_items} sản phẩm",
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
            fg_color="#F8F9FA" if self.current_page > 1 else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.previous_page if self.current_page > 1 else None
        )
        prev_button.pack(side="left", padx=(0, 5))
        
        visible_pages = 5
        start_page = max(1, min(self.current_page - visible_pages // 2,
                               total_pages - visible_pages + 1))
        end_page = min(start_page + visible_pages - 1, total_pages)
        
        for page in range(start_page, end_page + 1):
            is_current = page == self.current_page
            page_button = ctk.CTkButton(
                right_frame,
                text=str(page),
                width=30,
                height=30,
                fg_color="#006EC4" if is_current else "#F8F9FA",
                text_color="white" if is_current else "#16151C",
                hover_color="#0059A1" if is_current else "#E8E9EA",
                command=lambda p=page: self.go_to_page(p)
            )
            page_button.pack(side="left", padx=2)
        
        next_button = ctk.CTkButton(
            right_frame,
            text="",
            image=self.chevron_right_image,
            width=30,
            height=30,
            fg_color="#F8F9FA" if self.current_page < total_pages else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.next_page if self.current_page < total_pages else None
        )
        next_button.pack(side="left", padx=(5, 0))

    def previous_page(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Giảm số trang hiện tại nếu > 1
            - Tải lại danh sách sản phẩm với trang mới
        """
        if self.current_page > 1:
            self.current_page -= 1
            self.load_products()

    def next_page(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Tăng số trang hiện tại
            - Tải lại danh sách sản phẩm với trang mới
        """
        self.current_page += 1
        self.load_products()

    def go_to_page(self, page):
        """
        + Input:
            - page: Số trang cần chuyển đến
        + Output: Không có
        + Side effects:
            - Cập nhật số trang hiện tại
            - Tải lại danh sách sản phẩm với trang mới
        """
        self.current_page = page
        self.load_products()

    def show_add_dialog(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog thêm sản phẩm mới nếu có quyền
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        """Show dialog to add a new product"""
        dialog = ProductDialog(
            self,
            on_save=self.save_product
        )

    def show_edit_dialog(self, product):
        """
        + Input:
            - product: Từ điển chứa thông tin sản phẩm cần sửa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog sửa sản phẩm nếu có quyền
            - Điền sẵn thông tin sản phẩm vào form
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        print("product", product)
        """Show dialog to edit a product"""
        # Create product data dictionary with the required format
        product_data = {
            "ma_san_pham": product["ma_san_pham"],
            "ten": product["ten"],
            "mo_ta": product["mo_ta"],
            "don_gia": product["don_gia"],
            "ma_danh_muc": product["ma_danh_muc"],
            "ma_ncc": product["ma_ncc"]
        }
        
        dialog = ProductDialog(
            self,
            product=product_data,
            on_save=self.save_product,
        )

    def delete_product(self, product):
        """
        + Input:
            - product: Từ điển chứa thông tin sản phẩm cần xóa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog xác nhận xóa nếu có quyền
            - Xóa sản phẩm và tải lại danh sách nếu người dùng xác nhận
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        """Show confirmation dialog and delete product"""
        def handle_delete():
            try:
                success, message = self.controller.xoaSanPham(product["ma_san_pham"])
                if success:
                    self.load_products()
                else:
                    from tkinter import messagebox
                    messagebox.showerror("Lỗi", message)
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", str(e))
        
        DeleteDialog(
            self,
            product["ten"],
            on_confirm=handle_delete
        )

    def show_filter_dialog(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Mở dialog lọc với các tùy chọn:
                + Sắp xếp tên sản phẩm (A-Z, Z-A)
                + Sắp xếp giá (Thấp đến cao, Cao đến thấp)
            - Tạo các nút radio cho mỗi tùy chọn
            - Tạo nút Hủy và Áp dụng
        """
        dialog = CenterDialog(self, "Lọc Sản Phẩm", "400x300")
        
        self.name_sort = tk.StringVar(value="none")
        self.price_sort = tk.StringVar(value="none")
        
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        name_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Tên Sản Phẩm",
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
        
        price_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=(0, 20))
        
        price_label = ctk.CTkLabel(
            price_frame,
            text="Giá",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        price_label.pack(anchor="w", pady=(0, 10))
        
        price_options_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        price_options_frame.pack(fill="x")
        
        price_all = ctk.CTkRadioButton(
            price_options_frame,
            text="Tất Cả",
            variable=self.price_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        price_all.pack(side="left", padx=(0, 15))
        
        price_asc = ctk.CTkRadioButton(
            price_options_frame,
            text="Thấp đến Cao",
            variable=self.price_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        price_asc.pack(side="left", padx=(0, 15))
        
        price_desc = ctk.CTkRadioButton(
            price_options_frame,
            text="Cao đến Thấp",
            variable=self.price_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        price_desc.pack(side="left")
        
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
            command=lambda: self.apply_filters(dialog)
        )
        apply_button.pack(side="left")

    def apply_filters(self, dialog):
        """
        + Input:
            - dialog: Dialog lọc đang hiển thị
        + Output: Không có
        + Side effects:
            - Đóng dialog lọc
            - Reset về trang đầu tiên
            - Cập nhật các giá trị lọc
            - Tải lại danh sách sản phẩm theo điều kiện lọc mới
        """
        dialog.destroy()
        self.current_page = 1
        self.name_sort_value = self.name_sort.get()
        self.price_sort_value = self.price_sort.get()
        self.load_products()

    def save_product(self, data):
        """
        + Input:
            - data: Từ điển chứa thông tin sản phẩm cần lưu:
                + ma_san_pham: Mã sản phẩm (nếu là cập nhật)
                + ten: Tên sản phẩm
                + mo_ta: Mô tả sản phẩm
                + don_gia: Giá sản phẩm
                + ma_danh_muc: Mã danh mục
                + ma_ncc: Mã nhà cung cấp
        + Output: Không có
        + Side effects:
            - Kiểm tra và xử lý dữ liệu đầu vào
            - Thêm mới hoặc cập nhật sản phẩm trong database
            - Tải lại danh sách sản phẩm nếu thành công
            - Hiển thị thông báo lỗi nếu thất bại
        + Raises:
            - ValueError khi giá không hợp lệ
            - Exception khi lưu sản phẩm thất bại
        """
        try:
            try:
                price = float(data['don_gia'])
                if price < 0 or price > 999999999:
                    raise ValueError("Giá phải nằm trong khoảng từ 0 đến 999,999,999 ₫")
                price = round(price, 0)
            except ValueError as e:
                if "phải nằm trong khoảng" in str(e):
                    raise e
                raise ValueError("Giá phải là một số hợp lệ")

            product_data = {
                'ten': data['ten'],
                'mo_ta': data['mo_ta'],
                'don_gia': price,
                'ma_danh_muc': data['ma_danh_muc'],
                'ma_ncc': data['ma_ncc']
            }

            if "ma_san_pham" in data:
                success = self.controller.capNhatSanPham(data["ma_san_pham"], product_data)
            else:
                success = self.controller.themSanPham(product_data)
            
            if success:
                self.load_products()
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Failed to save product")
            
        except ValueError as e:
            from tkinter import messagebox
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to save product: {str(e)}")

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ctk.CTkLabel(
                tooltip,
                text=text,
                fg_color="#16151C",
                text_color="white",
                corner_radius=6
            )
            label.pack(padx=10, pady=5)
            
            def hide_tooltip(event):
                tooltip.destroy()
            
            widget.bind("<Leave>", hide_tooltip)
            tooltip.bind("<Leave>", hide_tooltip)
            
        widget.bind("<Enter>", show_tooltip)
