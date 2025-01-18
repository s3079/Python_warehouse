import customtkinter as ctk
from PIL import Image
from pathlib import Path
from app.controllers.order_controller import OrderController
from app.views.dialogs.order_dialog import OrderDialog
from app.views.dialogs.center_dialog import CenterDialog
from app.views.dialogs.add_order_dialog import AddOrderDialog
from app.views.dialogs.edit_order_dialog import EditOrderDialog

class OrdersPage(ctk.CTkFrame):
    def __init__(self, parent, controller, user_data, can_edit=True):
        super().__init__(parent, fg_color="transparent")
        self.controller = OrderController()
        self.can_edit = can_edit
        self.user_data = user_data
        
        # Get user_id from parent (AdminDashboard)
        self.ma_nguoi_dung = self.user_data["ma_nguoi_dung"]  # Updated from user_id
        
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0


        # Load icons
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
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create top section with search and buttons
        top_section = ctk.CTkFrame(self, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 20))
        top_section.grid_columnconfigure(1, weight=1)
        
        
        # Create buttons container
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # # Add filter button
        # filter_button = ctk.CTkButton(
        #     buttons_frame,
        #     text="Filter",
        #     image=self.filter_icon,
        #     compound="left",
        #     fg_color="#F8F9FA",
        #     text_color="#16151C",
        #     hover_color="#E8E9EA",
        #     width=100,
        #     height=45,
        #     corner_radius=8,
        #     # command=self.show_filter_dialog
        # )
        # filter_button.pack(side="left", padx=(0, 10))
        
        # Add new order button
        new_order_button = ctk.CTkButton(
            buttons_frame,
            text="Thêm Đơn Hàng",
            image=self.plus_icon,
            compound="left",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=140,
            height=45,
            corner_radius=8,
            command=self.show_add_order_dialog
        )
        new_order_button.pack(side="left")
        
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
            {"name": "Mã đơn hàng", "key": "ma_don_hang", "width": 100},
            {"name": "Ngày đặt", "key": "ngay_dat", "width": 150},        
            {"name": "Tổng tiền", "key": "tong_tien", "width": 100},      
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
        self.load_orders()
    


    def load_orders(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Xóa nội dung bảng hiện tại
            - Tải và hiển thị danh sách đơn hàng mới
            - Tạo các nút thao tác (sửa, xóa) cho mỗi đơn hàng
            - Định dạng hiển thị tiền tệ
            - Cập nhật điều khiển phân trang
        """
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Calculate pagination
        offset = (self.current_page - 1) * self.items_per_page
        
        # Get orders from controller with pagination
        orders, total_count = self.controller.layDonHangPhanTrang(
            offset=offset,
            limit=self.items_per_page,
        )
        
        self.total_items = total_count
        total_pages = -(-total_count // self.items_per_page)  # Ceiling division
        
        # Configure grid columns for content frame
        self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)

        print(orders)
        
        # Create rows for each order
        for i, order in enumerate(orders):
            row_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color="white" if i % 2 == 0 else "#F8F9FA",
                height=50
            )
            row_frame.pack(fill="x")
            
            # Bind click event to show order details
            row_frame.bind("<Button-1>", lambda e, o=order: self.show_order_details(o))
            
            # Add order data
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
                        command=lambda o=order: self.edit_order(o)
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
                        command=lambda o=order: self.delete_order(o)
                    )
                    delete_btn.pack(side="left")
                    
                elif col["key"] == "tong_tien":
                    # Format total with VND currency
                    value = f"{float(order[col['key']]):,.0f} ₫"
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                elif col["key"] == "ngay_dat":
                    # Format date as yyyy-mm-dd
                    from datetime import datetime
                    date_obj = datetime.strptime(str(order[col['key']]), '%Y-%m-%d %H:%M:%S')
                    value = date_obj.strftime('%Y-%m-%d')
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                else:
                    value = str(order[col["key"]])
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

    def create_pagination_controls(self, total_pages):
        """
        + Input:
            - total_pages: Tổng số trang
        + Output: Không có
        + Side effects:
            - Tạo hoặc cập nhật khung điều khiển phân trang
            - Hiển thị thông tin số lượng bản ghi (ví dụ: "Hiển thị 1-10 trong 100 đơn hàng")
            - Tạo nút Previous nếu không phải trang đầu
            - Tạo các nút số trang (tối đa 5 nút)
            - Tạo nút Next nếu không phải trang cuối
            - Cập nhật trạng thái active/inactive của các nút
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
            text=f"Hiển thị {start_index}-{end_index} trong {self.total_items} đơn hàng",
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
            - Tải lại danh sách đơn hàng với trang mới
        """
        if self.current_page > 1:
            self.current_page -= 1
            self.load_orders()

    def next_page(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Tăng số trang hiện tại
            - Tải lại danh sách đơn hàng với trang mới
        """
        self.current_page += 1
        self.load_orders()

    def go_to_page(self, page):
        """
        + Input:
            - page: Số trang cần chuyển đến
        + Output: Không có
        + Side effects:
            - Cập nhật số trang hiện tại
            - Tải lại danh sách đơn hàng với trang mới
        """
        self.current_page = page
        self.load_orders()

    def edit_order(self, order_data):
        """
        + Input:
            - order_data: Từ điển chứa thông tin đơn hàng cần sửa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog sửa đơn hàng nếu có quyền
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = EditOrderDialog(self, order_data, on_save=self.update_order)

    def update_order(self, data):
        """
        + Input:
            - data: Từ điển chứa thông tin cập nhật đơn hàng
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Cập nhật đơn hàng trong database
            - Tải lại danh sách đơn hàng nếu thành công
            - Hiển thị thông báo thành công/thất bại
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        print("data:", data)
        try:
            success = self.controller.capNhatDonHang(data)
            if success:
                self.load_orders()  # Refresh the table to show updated data
                from tkinter import messagebox
                messagebox.showinfo("Success", "Order updated successfully!")
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Failed to update order")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e))

    def delete_order(self, order):
        """
        + Input:
            - order: Từ điển chứa thông tin đơn hàng cần xóa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog xác nhận xóa với:
                + Icon cảnh báo
                + Thông báo xác nhận
                + Nút Hủy và Delete
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = CenterDialog(self, "Delete Order")
        
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
            text=f"Bạn có chắc chắn muốn xóa đơn hàng '{order['ma_don_hang']}'?\nHành động này không thể hoàn tác.",
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
            text="Delete",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.confirm_delete(dialog, order)
        )
        delete_button.pack(side="right")

    def save_order_changes(self, dialog, ma_don_hang, ngay_dat, tong_tien):
        """
        + Input:
            - dialog: Dialog đang hiển thị
            - ma_don_hang: Mã đơn hàng cần cập nhật
            - ngay_dat: Ngày đặt hàng mới
            - tong_tien: Tổng tiền mới
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Kiểm tra và xử lý dữ liệu đầu vào
            - Cập nhật đơn hàng trong database
            - Đóng dialog và tải lại danh sách nếu thành công
            - Hiển thị thông báo lỗi nếu thất bại
        + Raises:
            - ValueError khi dữ liệu không hợp lệ
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        try:
            if not ngay_dat:
                raise ValueError("Ngày đặt là bắt buộc")
            try:
                tong_tien = float(tong_tien.replace(',', '').replace('₫', '').strip())
                if tong_tien < 0:
                    raise ValueError
                if tong_tien > 999999999:
                    raise ValueError("Tổng tiền không được vượt quá 999,999,999 ₫")
            except ValueError as e:
                if "không được vượt quá" in str(e):
                    raise e
                raise ValueError("Tổng tiền phải là số hợp lệ")
            
            success = self.controller.capNhatDonHang(ma_don_hang, {
                "ngay_dat": ngay_dat,
                "tong_tien": tong_tien
            })
            
            if success:
                dialog.destroy()
                self.load_orders()  # Refresh the list
            else:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Cập nhật đơn hàng thất bại")
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e))

    def confirm_delete(self, dialog, order):
        """
        + Input:
            - dialog: Dialog xác nhận đang hiển thị
            - order: Từ điển chứa thông tin đơn hàng cần xóa
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Xóa đơn hàng khỏi database
            - Đóng dialog và tải lại danh sách nếu thành công
            - Hiển thị thông báo lỗi nếu thất bại
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        try:
            if self.controller.xoaDonHang(order["ma_don_hang"]):
                dialog.destroy()
                self.load_orders()  # Refresh the list
            else:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Xóa đơn hàng thất bại")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e))

    def show_order_details(self, order):
        """
        + Input:
            - order: Từ điển chứa thông tin đơn hàng cần xem
        + Output: Không có
        + Side effects:
            - Tải chi tiết đơn hàng từ database
            - Hiển thị dialog chi tiết nếu tải thành công
            - Hiển thị thông báo lỗi nếu thất bại
        """
        order_details = self.controller.layChiTietDonHang(order['ma_don_hang'])
        if order_details:
            dialog = OrderDialog(self, order=order_details)
            dialog.show()
        else:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", "Không thể tải chi tiết đơn hàng")

    def show_add_order_dialog(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Hiển thị thông báo nếu không có quyền
            - Mở dialog thêm đơn hàng mới nếu có quyền
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = AddOrderDialog(self, ma_nguoi_dung=self.ma_nguoi_dung, on_save=self.add_order)

    def add_order(self, order_data):
        """
        + Input:
            - order_data: Từ điển chứa thông tin đơn hàng mới
        + Output: Không có
        + Side effects:
            - Kiểm tra quyền chỉnh sửa
            - Thêm đơn hàng mới vào database
            - Tải lại danh sách đơn hàng nếu thành công
            - Hiển thị thông báo lỗi nếu thất bại
        """
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        try:
            success = self.controller.themDonHang(order_data)
            if success:
                self.load_orders()  # Refresh the list
            else:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Thêm đơn hàng thất bại")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e))
