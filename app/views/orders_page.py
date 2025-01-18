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
        
        self.ma_nguoi_dung = self.user_data["ma_nguoi_dung"]
        
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0


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
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        top_section = ctk.CTkFrame(self, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 20))
        top_section.grid_columnconfigure(1, weight=1)
        

        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
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
            command=self.hienThiFormThemDonHang
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

        self.table_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent"
        )
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        self.columns = [
            {"name": "Mã đơn hàng", "key": "ma_don_hang", "width": 100},
            {"name": "Ngày đặt", "key": "ngay_dat", "width": 150},        
            {"name": "Tổng tiền", "key": "tong_tien", "width": 100},      
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
        
        self.taiDonHang()
    


    def taiDonHang(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        offset = (self.current_page - 1) * self.items_per_page

        orders, total_count = self.controller.layDonHangPhanTrang(
            offset=offset,
            limit=self.items_per_page,
        )
        
        self.total_items = total_count
        total_pages = -(-total_count // self.items_per_page)

        self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)

        for i, order in enumerate(orders):
            row_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color="white" if i % 2 == 0 else "#F8F9FA",
                height=50
            )
            row_frame.pack(fill="x")
            
            row_frame.bind("<Button-1>", lambda e, o=order: self.hienThiChiTietDonHang(o))

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
                        command=lambda o=order: self.suaDonHang(o)
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
                        command=lambda o=order: self.xoaDonHang(o)
                    )
                    delete_btn.pack(side="left")
                    
                elif col["key"] == "tong_tien":
                    value = f"{float(order[col['key']]):,.0f} ₫"
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                elif col["key"] == "ngay_dat":
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

            separator = ctk.CTkFrame(
                self.content_frame,
                fg_color="#E5E5E5",
                height=1
            )
            separator.pack(fill="x")

        self.taoNutPhanTrang(total_pages)

    def taoNutPhanTrang(self, total_pages):
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
            text=f"Hiển thị {start_index}-{end_index} trong {self.total_items} đơn hàng",
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
            command=self.trangTruoc if self.current_page > 1 else None
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
                command=lambda p=page: self.denTrang(p)
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
            command=self.trangTiepTheo if self.current_page < total_pages else None
        )
        next_button.pack(side="left", padx=(5, 0))

    def trangTruoc(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.taiDonHang()

    def trangTiepTheo(self):
        self.current_page += 1
        self.taiDonHang()

    def denTrang(self, page):
        self.current_page = page
        self.taiDonHang()

    def suaDonHang(self, order_data):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = EditOrderDialog(self, order_data, on_save=self.capNhatDonHang)

    def capNhatDonHang(self, data):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        try:
            success = self.controller.capNhatDonHang(data)
            if success:
                self.taiDonHang()
                from tkinter import messagebox
                messagebox.showinfo("Success", "Order updated successfully!")
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Failed to update order")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", str(e))

    def xoaDonHang(self, order):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = CenterDialog(self, "Delete Order")
        
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        warning_label = ctk.CTkLabel(
            content_frame,
            text="⚠️ Cảnh báo",
            font=("", 16, "bold"),
            text_color="#e03137"
        )
        warning_label.pack(pady=(0, 10))

        message_label = ctk.CTkLabel(
            content_frame,
            text=f"Bạn có chắc chắn muốn xóa đơn hàng '{order['ma_don_hang']}'?\nHành động này không thể hoàn tác.",
            font=("", 13),
            text_color="#16151C"
        )
        message_label.pack(pady=(0, 20))

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
        
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Delete",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.xacNhanXoa(dialog, order)
        )
        delete_button.pack(side="right")

    def luuThayDoiDonHang(self, dialog, ma_don_hang, ngay_dat, tong_tien):
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
                self.taiDonHang()
            else:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Cập nhật đơn hàng thất bại")
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e))

    def xacNhanXoa(self, dialog, order):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        try:
            if self.controller.xoaDonHang(order["ma_don_hang"]):
                dialog.destroy()
                self.taiDonHang() 
            else:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Xóa đơn hàng thất bại")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e))

    def hienThiChiTietDonHang(self, order):
        order_details = self.controller.layChiTietDonHang(order['ma_don_hang'])
        if order_details:
            dialog = OrderDialog(self, order=order_details)
            dialog.show()
        else:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", "Không thể tải chi tiết đơn hàng")

    def hienThiFormThemDonHang(self):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        dialog = AddOrderDialog(self, ma_nguoi_dung=self.ma_nguoi_dung, on_save=self.themDonHang)

    def themDonHang(self, order_data):
        if not self.can_edit:
            from tkinter import messagebox
            messagebox.showinfo("Thông báo", "Tính năng dành cho người quản lý")
            return
        try:
            success = self.controller.themDonHang(order_data)
            if success:
                self.taiDonHang()
            else:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Thêm đơn hàng thất bại")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", str(e))
