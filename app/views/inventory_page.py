import customtkinter as ctk
from PIL import Image
from pathlib import Path
from app.controllers.inventory_controller import InventoryController
from app.views.dialogs.inventory_dialog import InventoryDialog

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller, can_edit=True):
        super().__init__(parent, fg_color="transparent")
        self.controller = InventoryController()
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
        self.chevron_left_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-left.png')),
            size=(20, 20)
        )
        self.chevron_right_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-right.png')),
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
            placeholder_text="Tìm kiếm...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        self.search_entry.bind("<Return>", self.on_search)
        
       
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        
    
        new_inventory_button = ctk.CTkButton(
            buttons_frame,
            text="Thêm",
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
        new_inventory_button.pack(side="left")
        
     
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
            {"name": "Tên sản phẩm", "key": "ten_san_pham", "width": 200},
            {"name": "Số lượng", "key": "so_luong", "width": 100},
            {"name": "Ngày nhập kho", "key": "ngay_nhap_cuoi", "width": 150},
            {"name": "Thao tác", "key": "actions", "width": 120}
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
        
        self.load_inventory()
    
    def on_search(self, event=None):
        """
        + Input:
            - event: Sự kiện tìm kiếm (tùy chọn)
        + Output: Không có
        + Side effects:
            - Cập nhật từ khóa tìm kiếm
            - Reset về trang đầu tiên
            - Tải lại danh sách kho hàng theo điều kiện tìm kiếm mới
        """
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1
        self.load_inventory()

    def load_inventory(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Xóa nội dung bảng hiện tại
            - Tải và hiển thị danh sách kho hàng mới
            - Cập nhật điều khiển phân trang
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        offset = (self.current_page - 1) * self.items_per_page
        
        inventory, total_count = self.controller.layKhoHangPhanTrang(
            offset=offset,
            limit=self.items_per_page,
            search_query=self.search_query
        )
        
        self.total_items = total_count
        total_pages = -(-total_count // self.items_per_page) 
        

        self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)
        
        for i, item in enumerate(inventory):
            row_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color="white" if i % 2 == 0 else "#F8F9FA",
                height=50
            )
            row_frame.pack(fill="x")
            
            for j, col in enumerate(self.columns):
                self.create_row(row_frame, item, col, j)
            
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
            - Tạo hoặc cập nhật điều khiển phân trang
            - Hiển thị thông tin số lượng bản ghi
            - Tạo các nút điều hướng trang
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
            text=f"Hiện thị {start_index}-{end_index} trong {self.total_items} kho hàng",
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
            - Giảm số trang hiện tại
            - Tải lại danh sách kho hàng với trang mới
        """
        if self.current_page > 1:
            self.current_page -= 1
            self.load_inventory()

    def next_page(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Tăng số trang hiện tại
            - Tải lại danh sách kho hàng với trang mới
        """
        self.current_page += 1
        self.load_inventory()

    def go_to_page(self, page):
        """
        + Input:
            - page: Số trang cần chuyển đến
        + Output: Không có
        + Side effects:
            - Cập nhật số trang hiện tại
            - Tải lại danh sách kho hàng với trang mới
        """
        self.current_page = page
        self.load_inventory()

    def show_add_dialog(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog thêm kho hàng nếu có quyền
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        InventoryDialog(self, on_save=self.add_inventory_item)

    def add_inventory_item(self, data):
        """
        + Input:
            - data: Từ điển chứa thông tin kho hàng mới
        + Output: Không có
        + Side effects:
            - Thêm kho hàng mới vào database
            - Tải lại danh sách kho hàng nếu thành công
            - In thông báo lỗi nếu thất bại
        """
        success, message = self.controller.themKhoHang(data)
        if success:
            self.load_inventory()
        else:
            print(message)

    def show_filter_dialog(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects: Hiển thị dialog tùy chọn lọc
        """

    def create_row(self, row_frame, item, col, j):
        """
        + Input:
            - row_frame: Frame chứa dòng dữ liệu
            - item: Từ điển chứa thông tin kho hàng
            - col: Từ điển chứa thông tin cột
            - j: Chỉ số cột
        + Output: Không có
        + Side effects: Tạo và hiển thị các ô dữ liệu trong dòng
        """
        if col["key"] == "actions":
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=j, padx=10, pady=10, sticky="w")
      
            edit_button = ctk.CTkButton(
                actions_frame,
                text="",
                image=self.edit_icon,
                width=30,
                height=30,
                fg_color="#006EC4",
                text_color="white",
                hover_color="#0059A1",
                command=lambda: self.edit_inventory(item)
            )
            edit_button.pack(side="left", padx=(0, 5))
            
    
            delete_button = ctk.CTkButton(
                actions_frame,
                text="",
                image=self.trash_icon,
                width=30,
                height=30,
                fg_color="#e03137",
                text_color="white",
                hover_color="#b32429",
                command=lambda: self.delete_inventory(item)
            )
            delete_button.pack(side="left")
        elif col["key"] == "ngay_nhap_cuoi":
            from datetime import datetime
            date_value = item.get(col["key"])
            if date_value:
                date_obj = datetime.strptime(str(date_value), '%Y-%m-%d %H:%M:%S')
                value = date_obj.strftime('%Y-%m-%d')
            else:
                value = ""
            label = ctk.CTkLabel(
                row_frame,
                text=value,
                anchor="w",
                width=col["width"]
            )
            label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
        else:
            value = str(item.get(col["key"], ""))
            label = ctk.CTkLabel(
                row_frame,
                text=value,
                anchor="w",
                width=col["width"]
            )
            label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")

    def edit_inventory(self, inventory):
        """
        + Input:
            - inventory: Từ điển chứa thông tin kho hàng cần sửa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog sửa kho hàng nếu có quyền
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        def handle_save(data):
            try:
                print("data--", data)
                success = self.controller.capNhatKhoHang(data)
                if success:
                    self.load_inventory() 
                else:
                    from tkinter import messagebox
                    messagebox.showerror("Lỗi", "Cập nhật kho hàng thất bại")
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", str(e))
        
        from app.views.dialogs.inventory_dialog import InventoryDialog
        InventoryDialog(self, inventory, on_save=handle_save)

    def delete_inventory(self, inventory):
        """
        + Input:
            - inventory: Từ điển chứa thông tin kho hàng cần xóa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog xác nhận xóa nếu có quyền
            - Xóa kho hàng và tải lại danh sách nếu người dùng xác nhận
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        from app.views.dialogs.delete_dialog import DeleteDialog
        
        def handle_delete():
            try:
                success = self.controller.xoaKhoHang(inventory["ma_kho"])
                if success:
                    self.load_inventory()
                else:
                    from tkinter import messagebox
                    messagebox.showerror("Lỗi", "Xóa kho hàng thất bại")
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", str(e))
        
        DeleteDialog(
            self,
            f"kho hàng của sản phẩm '{inventory['ten_san_pham']}'",
            on_confirm=handle_delete
        )