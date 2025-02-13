import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from PIL import Image
from app.views.products_page import ProductsPage
from app.views.categories_page import CategoriesPage
from app.views.inventory_page import InventoryPage
from app.views.supplier_page import SupplierPage
from app.views.orders_page import OrdersPage


class ManagerDashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data

        ctk.set_appearance_mode("light")

        self.title('Quản Lý Kho')
        self.geometry('1200x700')
        self.configure(fg_color="white")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self, fg_color="white")
        main_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(main_container, fg_color="#E8FAFF", corner_radius=20)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 30))
        sidebar.grid_columnconfigure(0, weight=1)

        sidebar.grid_propagate(False)
        sidebar.configure(width=280)

        self.buttons = []
        self.icons = {}
        self.active_icons = {}

        icon_files = {
            'Sản Phẩm': 'products.png',
            'Danh Mục': 'category.png',
            'Kho': 'inventory.png',
            'Nhà Cung Cấp': 'supplier.png',
            'Đơn Hàng': 'order.png',
            'Tài Khoản': 'users.png',
            'Đăng Xuất': 'logout.png'
        }

        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'

        sidebar_content = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_content.pack(fill="both", expand=True, padx=20, pady=20)

        logo_frame = ctk.CTkFrame(sidebar_content, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(0, 30))

        logo_path = str(Path(__file__).parent.parent.parent / 'assets' / 'logo.png')
        logo_image = Image.open(logo_path)
        logo = ctk.CTkImage(
            light_image=logo_image,
            size=(32, 32)
        )

        logo_label = ctk.CTkLabel(
            logo_frame,
            image=logo,
            text="",
        )
        logo_label.pack(side="left", padx=(0, 10))

        project_name = ctk.CTkLabel(
            logo_frame,
            text="QLKH",
            font=("", 20, "bold"),
            text_color="#16151C"
        )
        project_name.pack(side="left")

        menu_container = ctk.CTkFrame(sidebar_content, fg_color="transparent")
        menu_container.pack(fill="both", expand=True)

        sidebar_items = ['Sản Phẩm', 'Danh Mục', 'Kho', 'Nhà Cung Cấp', 'Đơn Hàng']
        for item in sidebar_items:
            icon_path = str(assets_path / icon_files[item])
            icon_image = Image.open(icon_path)

            active_image = icon_image.copy()
            active_image = active_image.convert('RGBA')
            data = active_image.getdata()
            new_data = []
            for item_data in data:
                if item_data[3] != 0:
                    new_data.append((17, 24, 39, item_data[3]))
                else:
                    new_data.append(item_data)
            active_image.putdata(new_data)

            normal_icon = ctk.CTkImage(
                light_image=icon_image,
                size=(24, 24)
            )
            active_icon = ctk.CTkImage(
                light_image=active_image,
                size=(24, 24)
            )

            self.icons[item] = normal_icon
            self.active_icons[item] = active_icon

            button = ctk.CTkButton(
                menu_container,
                text=item,
                command=lambda i=item: self.show_page(i),
                fg_color="transparent",
                text_color="#16151C",
                image=normal_icon,
                compound="left",
                anchor="w",
                height=40,
                corner_radius=8,
                font=("", 13)
            )
            button.pack(fill='x', pady=5)
            self.buttons.append(button)

        logout_frame = ctk.CTkFrame(sidebar_content, fg_color="transparent", height=50)
        logout_frame.pack(fill="x", side="bottom")

        logout_icon_path = str(assets_path / 'logout.png')
        logout_icon_image = Image.open(logout_icon_path)

        red_icon = logout_icon_image.copy()
        red_icon = red_icon.convert('RGBA')
        data = red_icon.getdata()
        new_data = []
        for item in data:
            if item[3] != 0:
                new_data.append((255, 72, 66, item[3]))
            else:
                new_data.append(item)
        red_icon.putdata(new_data)

        logout_icon = ctk.CTkImage(
            light_image=red_icon,
            size=(24, 24)
        )

        logout_button = ctk.CTkButton(
            logout_frame,
            text="Đăng xuất",
            command=self.logout,
            fg_color="transparent",
            text_color="#FF4842",
            image=logout_icon,
            compound="left",
            anchor="w",
            height=40,
            corner_radius=8,
            font=("", 13),
            hover=True,
            hover_color="#FFE8E7"
        )
        logout_button.pack(fill="x")

        right_container = ctk.CTkFrame(main_container, fg_color="transparent")
        right_container.grid(row=0, column=1, sticky="nsew")
        right_container.grid_rowconfigure(1, weight=1)
        right_container.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(right_container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        header.grid_columnconfigure(1, weight=1)

        self.page_title = ctk.CTkLabel(
            header,
            text="Products",
            font=("", 24, "bold"),
            text_color="#16151C"
        )
        self.page_title.grid(row=0, column=0, sticky="w")

        user_info_frame = ctk.CTkFrame(
            header,
            fg_color="transparent",
            border_color="#F0F0F0",
            border_width=2,
            corner_radius=8
        )
        user_info_frame.grid(row=0, column=2, sticky="e", padx=(20, 0))

        user_details_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        user_details_frame.pack(side="left", padx=10, pady=2)

        username_label = ctk.CTkLabel(
            user_details_frame,
            text=user_data["ten_dang_nhap"],
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        username_label.pack(anchor="w")

        role_label = ctk.CTkLabel(
            user_details_frame,
            text=user_data["ho_ten"],
            font=("", 12),
            text_color="#6F6E77"
        )
        role_label.pack(anchor="w")

        chevron_path = str(assets_path / 'chevron-down.png')
        chevron_image = Image.open(chevron_path)
        chevron_icon = ctk.CTkImage(
            light_image=chevron_image,
            size=(16, 16)
        )

        chevron_label = ctk.CTkLabel(
            user_info_frame,
            text="",
            image=chevron_icon
        )
        chevron_label.pack(side="right", padx=10, pady=8)

        self.content_area = ctk.CTkFrame(right_container, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        self.bind("<Configure>", self.on_resize)

        self.show_page('Sản Phẩm')

    def logout(self):
        """
        + Input: Không có
        + Output: Không có
        + Side effects:
            - Hiển thị hộp thoại xác nhận đăng xuất
            - Nếu người dùng xác nhận:
                + Đóng cửa sổ dashboard
                + Mở lại màn hình đăng nhập
        """
        from tkinter import messagebox

        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"):
            self.destroy()
            from app.views.login_view import LoginView
            root = tk.Tk()
            login_screen = LoginView(root)
            root.mainloop()

    def on_resize(self, event):
        """
        + Input:
            - event: Sự kiện thay đổi kích thước cửa sổ
        + Output: Không có
        + Side effects:
            - Cập nhật lại giao diện khi cửa sổ thay đổi kích thước
        """
        self.update_idletasks()

    def apply_opacity(self, hex_color, opacity):
        """
        + Input:
            - hex_color: Mã màu hex (VD: "#FFFFFF")
            - opacity: Độ trong suốt (0.0 - 1.0)
        + Output: Mã màu hex với độ trong suốt được áp dụng
        + Side effects: Không có
        """
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        return f'#{int(rgb[0])}{int(rgb[1])}{int(rgb[2])}{int(opacity * 255):02x}'

    def show_page(self, page_name):
        """
        + Input:
            - page_name: Tên trang cần hiển thị (VD: "Sản Phẩm", "Danh Mục",...)
        + Output: Không có
        + Side effects:
            - Cập nhật trạng thái active của nút menu
            - Thay đổi màu sắc và icon của nút được chọn
            - Cập nhật tiêu đề trang
            - Xóa nội dung trang cũ
            - Tạo và hiển thị trang mới tương ứng với page_name
            - Truyền quyền chỉnh sửa (can_edit=True) cho tất cả các trang
            - Truyền thông tin người dùng cho trang Đơn hàng
        """
        for button in self.buttons:
            button_text = button.cget("text")
            button.configure(
                fg_color="transparent",
                text_color="#16151C",
                image=self.icons[button_text],
                font=("", 13)
            )

        active_button = next(btn for btn in self.buttons if btn.cget("text") == page_name)
        active_button.configure(
            fg_color="#C9F1FF",
            text_color="#006EC4",
            image=self.active_icons[page_name],
            font=("", 13, "bold")
        )

        self.page_title.configure(text=page_name)

        for widget in self.content_area.winfo_children():
            widget.destroy()

        if page_name == "Sản Phẩm":
            page = ProductsPage(self.content_area, self, can_edit=True)
        elif page_name == "Danh Mục":
            page = CategoriesPage(self.content_area, self, can_edit=True)
        elif page_name == "Kho":
            page = InventoryPage(self.content_area, self, can_edit=True)
        elif page_name == "Nhà Cung Cấp":
            page = SupplierPage(self.content_area, self, can_edit=True)
        elif page_name == "Đơn Hàng":
            page = OrdersPage(self.content_area, self, self.user_data, can_edit=True)
        else:
            page = ctk.CTkLabel(self.content_area, text=f'{page_name} Page (Content coming soon...)')

        page.pack(expand=True, fill="both")


# if __name__ == '__main__':
#     test_user_data = {"username": "Mathias"}
#     app = AdminDashboard(user_data=test_user_data)
#     app.mainloop()