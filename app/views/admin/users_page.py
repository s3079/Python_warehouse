import customtkinter as ctk
from app.controllers.user_controller import UserController
from PIL import Image
from pathlib import Path
import tkinter as tk

class UsersPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = UserController()
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0
        self.search_query = ""
        
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        self.search_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'search.png')),
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
        self.filter_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'filter.png')),
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
            placeholder_text="Tìm kiếm...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        self.search_entry.bind("<Return>", self.tim_kiem)
        
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
            {"name": "Tên đăng nhập", "key": "ten_dang_nhap", "width": 100},
            {"name": "Họ và tên", "key": "ho_ten", "width": 150},
            {"name": "Vai trò", "key": "ten_quyen", "width": 100},
            {"name": "Trạng thái", "key": "trang_thai", "width": 100},
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
        
        self.tai_danh_sach_nguoi_dung()
    
    def tim_kiem(self, event=None):
        """
        + Input:
            - event: Sự kiện tìm kiếm (tùy chọn)
        + Output: Không có
        + Side effects:
            - Cập nhật từ khóa tìm kiếm từ ô nhập liệu
            - Reset về trang đầu tiên
            - Tải lại danh sách người dùng theo từ khóa mới
        """
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1 
        self.tai_danh_sach_nguoi_dung()

    def tai_danh_sach_nguoi_dung(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Xóa nội dung bảng hiện tại
            - Tải và hiển thị danh sách người dùng mới
            - Tạo các nút thao tác (Duyệt/Từ chối) cho người dùng chưa duyệt
            - Tạo đường phân cách giữa các dòng
            - Cập nhật điều khiển phân trang
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        offset = (self.current_page - 1) * self.items_per_page
        
        users, total_count = self.controller.layNguoiDungPhanTrang(
            offset=offset,
            limit=self.items_per_page,
            search_query=self.search_query
        )
        
        self.total_items = total_count
        total_pages = -(-total_count // self.items_per_page)
        
        self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)
        
        for i, user in enumerate(users):
            row_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color="white" if i % 2 == 0 else "#F8F9FA",
                height=50
            )
            row_frame.pack(fill="x")
            
            for j, col in enumerate(self.columns):
                if col["key"] == "actions":
                    if user['ten_quyen'].lower() == 'administrator':
                        continue

                    # Create actions frame
                    actions_frame = ctk.CTkFrame(
                        row_frame,
                        fg_color="transparent"
                    )
                    actions_frame.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                    if user['da_duyet']:
                        set_role_btn = ctk.CTkButton(
                            actions_frame,
                            text="",    
                            image=self.edit_icon,
                            width=30, 
                            height=30,
                            fg_color="#006EC4",
                            hover_color="#0059A1",
                            command=lambda u=user: self.dat_vai_tro(u)
                        )
                        set_role_btn.pack(side="left", padx=(0, 5))
                        
                        delete_btn = ctk.CTkButton(
                            actions_frame,
                            text="",
                            image=self.trash_icon,
                            width=30,
                            height=30,
                            fg_color="#e03137",
                            hover_color="#b32429",
                            command=lambda u=user: self.xoa_nguoi_dung(u)
                        )
                        delete_btn.pack(side="left")
                    else:
                        approve_btn = ctk.CTkButton(
                            actions_frame,
                            text="Duyệt",
                            width=60,
                            height=30,
                            fg_color="#006EC4",
                            text_color="white",
                            hover_color="#0059A1",
                            command=lambda u=user: self.duyet_nguoi_dung(u)
                        )
                        approve_btn.pack(side="left", padx=(0, 5))
                        
                        reject_btn = ctk.CTkButton(
                            actions_frame,
                            text="Từ chối",
                            width=60,
                            height=30,
                            fg_color="#e03137",
                            text_color="white",
                            hover_color="#b32429",
                            command=lambda u=user: self.tu_choi_nguoi_dung(u)
                        )
                        reject_btn.pack(side="left")
                    
                else:
                    value = str(user.get(col["key"], "") or "")
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

        self.tao_dieu_khien_phan_trang(total_pages)

    def tao_dieu_khien_phan_trang(self, total_pages):
        """
        + Input:
            - total_pages: Tổng số trang
        + Output: Không có
        + Side effects:
            - Xóa điều khiển phân trang cũ nếu có
            - Tạo khung điều khiển phân trang mới
            - Hiển thị thông tin số lượng bản ghi (VD: "Hiển thị 1-10 trong 50 người dùng")
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
            text=f"Hiển thị {start_index}-{end_index} trong {self.total_items} người dùng",
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
            command=self.trang_truoc if self.current_page > 1 else None
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
                command=lambda p=page: self.den_trang(p)
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
            command=self.trang_sau if self.current_page < total_pages else None
        )
        next_button.pack(side="left", padx=(5, 0))

    def trang_truoc(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Giảm số trang hiện tại nếu > 1
            - Tải lại danh sách người dùng với trang mới
        """
        if self.current_page > 1:
            self.current_page -= 1
            self.tai_danh_sach_nguoi_dung()

    def trang_sau(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Tăng số trang hiện tại
            - Tải lại danh sách người dùng với trang mới
        """
        self.current_page += 1
        self.tai_danh_sach_nguoi_dung()

    def den_trang(self, page):
        """
        + Input:
            - page: Số trang cần chuyển đến
        + Output: Không có
        + Side effects:
            - Cập nhật số trang hiện tại
            - Tải lại danh sách người dùng với trang mới
        """
        self.current_page = page
        self.tai_danh_sach_nguoi_dung()

    def duyet_nguoi_dung(self, user):
        """
        + Input:
            - user: Từ điển chứa thông tin người dùng cần duyệt
        + Output: Không có
        + Side effects:
            - Gọi API duyệt người dùng
            - Tải lại danh sách người dùng nếu thành công
        """
        if self.controller.duyetNguoiDung(user["ma_nguoi_dung"]):
            self.tai_danh_sach_nguoi_dung()

    def tu_choi_nguoi_dung(self, user):
        """
        + Input:
            - user: Từ điển chứa thông tin người dùng cần từ chối
        + Output: Không có
        + Side effects:
            - Gọi API từ chối người dùng
            - Tải lại danh sách người dùng nếu thành công
        """
        if self.controller.tuChoiNguoiDung(user["ma_nguoi_dung"]):
            self.tai_danh_sach_nguoi_dung()

    def hien_thi_hop_thoai_loc(self):
        print("Đã mở hộp thoại lọc")

    def dat_vai_tro(self, user):
        """
        + Input:
            - user: Từ điển chứa thông tin người dùng cần đặt vai trò
        + Output: Không có
        + Side effects:
            - Mở dialog đặt vai trò với:
                + Hiển thị vai trò hiện tại
                + Radio buttons cho các vai trò (Người dùng/Quản lý)
                + Nút xác nhận thay đổi
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title("Đặt vai trò")
        dialog.geometry("300x200")
        
        current_role_label = ctk.CTkLabel(dialog, text=f"Vai trò hiện tại: {user.get('ten_quyen', 'Chưa xác định')}")
        current_role_label.pack(pady=10)
        
        label = ctk.CTkLabel(dialog, text="Chọn vai trò mới cho người dùng:")
        label.pack(pady=10)
        
        current_role = user.get("ten_quyen", "user")
        role_var = ctk.StringVar(value=current_role)
        
        radio_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        radio_frame.pack(pady=10)
        
        user_radio = ctk.CTkRadioButton(radio_frame, text="Người dùng", variable=role_var, value="user")
        manager_radio = ctk.CTkRadioButton(radio_frame, text="Quản lý", variable=role_var, value="manager")
        
        user_radio.pack(side="left", padx=10)
        manager_radio.pack(side="left", padx=10)
        
        confirm_button = ctk.CTkButton(
            dialog,
            text="Xác nhận",
            command=lambda: self.xac_nhan_thay_doi_vai_tro(user, role_var.get(), dialog)
        )
        confirm_button.pack(pady=10)

    def xac_nhan_thay_doi_vai_tro(self, user, new_role, dialog):
        """
        + Input:
            - user: Từ điển chứa thông tin người dùng
            - new_role: Vai trò mới ("user" hoặc "manager")
            - dialog: Dialog đang hiển thị
        + Output: Không có
        + Side effects:
            - Gọi API đặt vai trò mới
            - Đóng dialog nếu thành công
            - Tải lại danh sách người dùng
            - Hiển thị thông báo kết quả
        """
        if self.controller.datVaiTroNguoiDung(user["ma_nguoi_dung"], new_role):
            self.tai_danh_sach_nguoi_dung()
            dialog.destroy()
            tk.messagebox.showinfo("Thành công", "Đã cập nhật vai trò người dùng thành công.")
        else:
            tk.messagebox.showerror("Lỗi", "Không thể cập nhật vai trò người dùng.")

    def xoa_nguoi_dung(self, user):
        """
        + Input:
            - user: Từ điển chứa thông tin người dùng cần xóa
        + Output: Không có
        + Side effects:
            - Mở dialog xác nhận xóa với:
                + Thông báo xác nhận có tên người dùng
                + Cảnh báo không thể hoàn tác
                + Nút Hủy và Xóa
        """
        # Create confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Xác nhận xóa")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Message
        message = ctk.CTkLabel(
            dialog,
            text=f"Bạn có chắc chắn muốn xóa người dùng '{user['ho_ten']}'?\nHành động này không thể hoàn tác.",
            font=("", 13)
        )
        message.pack(pady=(20, 0))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(20, 20))
        buttons_frame.pack_propagate(False)
        
        # Container for right-aligned buttons
        button_container = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        button_container.pack(side="right")
        button_containerC = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        button_containerC.pack(side="left")
        # Cancel button
        cancel_button = ctk.CTkButton(
            button_containerC,
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
            button_container,
            text="Xóa",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.xac_nhan_xoa_nguoi_dung(dialog, user)
        )
        delete_button.pack(side="left")

    def xac_nhan_xoa_nguoi_dung(self, dialog, user):
        """
        + Input:
            - dialog: Dialog xác nhận đang hiển thị
            - user: Từ điển chứa thông tin người dùng cần xóa
        + Output: Không có
        + Side effects:
            - Gọi API xóa người dùng
            - Đóng dialog
            - Tải lại danh sách người dùng nếu thành công
            - Hiển thị thông báo kết quả
        """
        # Confirm and execute user deletion
        success, message = self.controller.xoaNguoiDung(user["ma_nguoi_dung"])
        if success:
            dialog.destroy()
            self.tai_danh_sach_nguoi_dung()
            tk.messagebox.showinfo("Thành công", message)
        else:
            tk.messagebox.showerror("Lỗi", message)
            dialog.destroy()
