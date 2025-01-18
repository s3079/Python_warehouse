import customtkinter as ctk
from PIL import Image
from pathlib import Path
import tkinter as tk
from app.controllers.supplier_controller import SupplierController
from app.views.admin.dialogs.supplier_dialog import SupplierDialog
from app.views.admin.dialogs.center_dialog import CenterDialog

class SupplierPage(ctk.CTkFrame):
    def __init__(self, parent, controller, can_edit=True):
        super().__init__(parent, fg_color="transparent")
        self.controller = SupplierController()
        self.can_edit = can_edit
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0
        self.search_query = ""
        self.name_sort_value = "none"
        self.contact_sort_value = "none"
        
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

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create top section with search and buttons
        top_section = ctk.CTkFrame(self, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 20))
        top_section.grid_columnconfigure(1, weight=1)
        
        # Create search frame
        search_frame = ctk.CTkFrame(
            top_section,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        search_frame.grid(row=0, column=0, sticky="w")
        
        # Add search icon and entry
        search_icon_label = ctk.CTkLabel(
            search_frame,
            text="",
            image=self.search_icon
        )
        search_icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm kiếm nhà cung cấp...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        self.search_entry.bind("<Return>", self.on_search)
        
        # Create buttons container
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add filter button
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
        
        # Add new supplier button
        new_supplier_button = ctk.CTkButton(
            buttons_frame,
            text='Thêm Nhà Cung Cấp',
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
        new_supplier_button.pack(side="left")
        
        # Create table container
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

        # Create scrollable frame for table
        self.table_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent"
        )
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        # Define column configurations
        self.columns = [
            {"name": "Tên nhà cung cấp", "key": "ten", "width": 200},
            {"name": "Email", "key": "email", "width": 200},
            {"name": "Điện thoại", "key": "dien_thoai", "width": 150},
            {"name": "Địa chỉ", "key": "dia_chi", "width": 200},
            {"name": "Thao tác", "key": "actions", "width": 100}
        ]
        
        # Create table header
        header_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="#F8F9FA",
            height=50
        )
        header_frame.pack(fill="x", expand=True)
        header_frame.pack_propagate(False)
        
        # Add header labels
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
            
        # Create frame for table content
        self.content_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True)
        
        # Load initial data
        self.load_suppliers()
    
    def on_search(self, event=None):
        """Handle search when Enter is pressed"""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1  # Reset to first page
        self.load_suppliers()

    def load_suppliers(self):
        """Load suppliers with current filters and pagination"""
        try:
            # Clear existing content
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Calculate pagination
            offset = (self.current_page - 1) * self.items_per_page
            
            # Get suppliers from controller with pagination and sorting
            suppliers, total_count = self.controller.layNhaCungCapPhanTrang(
                offset=offset,
                limit=self.items_per_page,
                search_query=self.search_query,
                name_sort=getattr(self, 'name_sort_value', 'none'),
                contact_sort=getattr(self, 'contact_sort_value', 'none')
            )
            
            self.total_items = total_count
            total_pages = -(-total_count // self.items_per_page)  # Ceiling division
            
            # Configure grid columns for content frame
            self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)
            
            # Create rows for each supplier
            for i, supplier in enumerate(suppliers):
                row_frame = ctk.CTkFrame(
                    self.content_frame,
                    fg_color="white" if i % 2 == 0 else "#F8F9FA",
                    height=50
                )
                row_frame.pack(fill="x")
                
                # Add supplier data
                for j, col in enumerate(self.columns):
                    if col["key"] == "actions":
                        # Create actions frame
                        actions_frame = ctk.CTkFrame(
                            row_frame,
                            fg_color="transparent"
                        )
                        actions_frame.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                        
                        # Edit button
                        edit_btn = ctk.CTkButton(
                            actions_frame,
                            text="",
                            image=self.edit_icon,
                            width=30,
                            height=30,
                            fg_color="#006EC4",
                            text_color="white",
                            hover_color="#0059A1",
                            command=lambda s=supplier: self.show_edit_dialog(s)
                        )
                        edit_btn.pack(side="left", padx=(0, 5))
                        
                        # Delete button
                        delete_btn = ctk.CTkButton(
                            actions_frame,
                            text="",
                            image=self.trash_icon,
                            width=30,
                            height=30,
                            fg_color="#e03137",
                            text_color="white",
                            hover_color="#b32429",
                            command=lambda s=supplier: self.delete_supplier(s)
                        )
                        delete_btn.pack(side="left")
                        
                    else:
                        # Regular text columns
                        value = str(supplier.get(col["key"], "") or "")
                        label = ctk.CTkLabel(
                            row_frame,
                            text=value,
                            anchor="w",
                            width=col["width"]
                        )
                        label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                
                # Add separator
                separator = ctk.CTkFrame(
                    self.content_frame,
                    fg_color="#E5E5E5",
                    height=1
                )
                separator.pack(fill="x")

            # Add pagination controls at the bottom
            self.create_pagination_controls(total_pages)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def create_pagination_controls(self, total_pages):
        """
        + Input:
            - total_pages: Tổng số trang
        + Output: Không có
        + Side effects:
            - Xóa điều khiển phân trang cũ nếu có
            - Tạo khung điều khiển phân trang mới
            - Hiển thị thông tin số lượng bản ghi (VD: "Hiển thị 1-10 của 50 nhà cung cấp")
            - Tạo nút Previous (mờ đi nếu ở trang đầu)
            - Tạo các nút số trang (tối đa 5 nút)
            - Tạo nút Next (mờ đi nếu ở trang cuối)
        """
        # Create or clear pagination frame
        if hasattr(self, 'pagination_frame'):
            for widget in self.pagination_frame.winfo_children():
                widget.destroy()
        else:
            self.pagination_frame = ctk.CTkFrame(self, fg_color="white", height=60)
            self.pagination_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
            self.pagination_frame.grid_propagate(False)
        
        # Create container for pagination elements
        controls_frame = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        controls_frame.pack(expand=True, fill="both")
        
        # Left side - showing entries info
        left_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=20)
        
        start_index = (self.current_page - 1) * self.items_per_page + 1
        end_index = min(start_index + self.items_per_page - 1, self.total_items)
        
        showing_label = ctk.CTkLabel(
            left_frame,
            text=f"Hiển thị {start_index}-{end_index} của {self.total_items} nhà cung cấp",
            text_color="#6F6E77"
        )
        showing_label.pack(side="left")
        
        # Right side - pagination buttons
        right_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=20)
        
        # Previous page button
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
        
        # Page number buttons
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
        
        # Next page button
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
            - Tải lại danh sách nhà cung cấp với trang mới
        """
        if self.current_page > 1:
            self.current_page -= 1
            self.load_suppliers()

    def next_page(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Tăng số trang hiện tại
            - Tải lại danh sách nhà cung cấp với trang mới
        """
        self.current_page += 1
        self.load_suppliers()

    def go_to_page(self, page):
        """
        + Input:
            - page: Số trang cần chuyển đến
        + Output: Không có
        + Side effects:
            - Cập nhật số trang hiện tại
            - Tải lại danh sách nhà cung cấp với trang mới
        """
        self.current_page = page
        self.load_suppliers()

    def show_add_dialog(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog thêm nhà cung cấp mới nếu có quyền
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        """Show dialog to add a new supplier"""
        dialog = SupplierDialog(
            self,
            on_save=self.save_supplier
        )

    def show_edit_dialog(self, supplier):
        """
        + Input:
            - supplier: Từ điển chứa thông tin nhà cung cấp cần sửa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog sửa nhà cung cấp nếu có quyền
            - Điền sẵn thông tin nhà cung cấp vào form
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        """Show dialog to edit a supplier"""
        dialog = SupplierDialog(
            self,
            supplier=supplier,
            on_save=self.save_supplier
        )

    def delete_supplier(self, supplier):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        """Show confirmation dialog and delete supplier"""
        dialog = CenterDialog(self, "Delete Supplier")
        
        # Create content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning icon or text
        warning_label = ctk.CTkLabel(
            content_frame,
            text="⚠️ Cảnh báo",
            font=("", 16, "bold"),
            text_color="#e03137"
        )
        warning_label.pack(pady=(0, 10))
        
        # Confirmation message
        message_label = ctk.CTkLabel(
            content_frame,
            text=f"Bạn có chắc chắn muốn xóa '{supplier['ten']}'?\nHành động này không thể hoàn tác.",
            font=("", 13),
            text_color="#16151C"
        )
        message_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
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
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Delete button
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Xóa",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.confirm_delete(dialog, supplier)
        )
        delete_button.pack(side="right")

    def confirm_delete(self, dialog, supplier):
        """
        + Input:
            - dialog: Dialog xác nhận đang hiển thị
            - supplier: Từ điển chứa thông tin nhà cung cấp cần xóa
        + Output: Không có
        + Side effects:
            - Xóa nhà cung cấp khỏi database
            - Đóng dialog xác nhận
            - Tải lại danh sách nhà cung cấp
            - Hiển thị thông báo lỗi nếu thất bại
        + Raises:
            - Exception khi xóa nhà cung cấp thất bại
        """
        try:
            self.controller.xoaNhaCungCap(supplier["ma_ncc"])
            dialog.destroy()
            self.load_suppliers()  # Refresh the list
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", f"Không thể xóa nhà cung cấp: {str(e)}")

    def show_filter_dialog(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Mở dialog lọc với các tùy chọn:
                + Sắp xếp theo tên (A-Z, Z-A)
                + Sắp xếp theo số điện thoại (A-Z, Z-A)
            - Tạo các nút radio cho mỗi tùy chọn
            - Tạo nút Hủy và Áp dụng
        """
        dialog = CenterDialog(self, "Lọc Nhà Cung Cấp", "400x300")
        
        # Store filter states
        self.name_sort = tk.StringVar(value="none")  # none, asc, desc
        self.contact_sort = tk.StringVar(value="none")  # none, asc, desc
        
        # Create main content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Name filter section
        name_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Tên",
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
        
        # Contact filter section
        contact_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        contact_frame.pack(fill="x", pady=(0, 20))
        
        contact_label = ctk.CTkLabel(
            contact_frame,
            text="Số Điện Thoại",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        contact_label.pack(anchor="w", pady=(0, 10))
        
        # Contact radio buttons
        contact_options_frame = ctk.CTkFrame(contact_frame, fg_color="transparent")
        contact_options_frame.pack(fill="x")
        
        contact_all = ctk.CTkRadioButton(
            contact_options_frame,
            text="Tất cả",
            variable=self.contact_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        contact_all.pack(side="left", padx=(0, 15))
        
        contact_asc = ctk.CTkRadioButton(
            contact_options_frame,
            text="A-Z",
            variable=self.contact_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        contact_asc.pack(side="left", padx=(0, 15))
        
        contact_desc = ctk.CTkRadioButton(
            contact_options_frame,
            text="Z-A",
            variable=self.contact_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        contact_desc.pack(side="left")
        
        # Add buttons
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
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
            command=dialog.destroy
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
            - Tải lại danh sách nhà cung cấp theo điều kiện lọc mới
        """
        dialog.destroy()
        self.current_page = 1  # Reset to first page
        self.name_sort_value = self.name_sort.get()
        self.contact_sort_value = self.contact_sort.get()
        self.load_suppliers()

    def save_supplier(self, supplier_data):
        """
        + Input:
            - supplier_data: Từ điển chứa thông tin nhà cung cấp cần lưu:
                + ma_ncc: Mã nhà cung cấp (nếu là cập nhật)
                + ten: Tên nhà cung cấp
                + email: Email liên hệ
                + dien_thoai: Số điện thoại
                + dia_chi: Địa chỉ
        + Output: Không có
        + Side effects:
            - Kiểm tra các trường bắt buộc
            - Thêm mới hoặc cập nhật nhà cung cấp trong database
            - Tải lại danh sách nhà cung cấp nếu thành công
            - Hiển thị thông báo lỗi nếu thất bại
        + Raises:
            - ValueError khi thiếu trường bắt buộc
            - Exception khi lưu nhà cung cấp thất bại
        """
        try:
            # Validate that all required fields are present
            required_fields = ["ten", "email", "dien_thoai", "dia_chi"]
            for field in required_fields:
                if field not in supplier_data:
                    raise ValueError(f"Missing required field: {field}")
                print("supplier_data", supplier_data)

            if "ma_ncc" in supplier_data:
                # Update existing supplier
                self.controller.capNhatNhaCungCap(
                    supplier_data  # Unpack the supplier_data dictionary
                )
            else:
                # Add new supplier
                self.controller.themNhaCungCap(
                    supplier_data
                )
            # Refresh the table
            self.load_suppliers()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to save supplier: {str(e)}")