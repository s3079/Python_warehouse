from pathlib import Path
import customtkinter as ctk
from PIL import Image
from app.controllers.user_controller import UserController
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent.parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class RegisterView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._controller = UserController()
        self.parent = parent
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Configure the parent window to be resizable
        parent.resizable(True, True)
        parent.minsize(1000, 600)
        
        # Configure the grid
        self.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        self._setup_ui()

    def _setup_ui(self):
        self.configure(fg_color="white")
        
        # Configure grid columns with weights
        self.grid_columnconfigure(0, weight=1)  # Left side
        self.grid_columnconfigure(1, weight=1)  # Right side
        self.grid_rowconfigure(0, weight=1)
        
        # Create left and right frames
        left_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        right_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 20))
        
        # Configure right frame grid
        right_frame.grid_columnconfigure(0, weight=1)
        for i in range(10):  # Approximate number of rows needed
            right_frame.grid_rowconfigure(i, weight=1)

        # Left side - Warehouse Image
        try:
            screen_height = self.winfo_screenheight()
            screen_width = self.winfo_screenwidth()
            warehouse_img = ctk.CTkImage(
                light_image=Image.open(relative_to_assets("warehouse.png")),
                size=(screen_width // 2, screen_height)  # Half width, full height
            )
            self.image_label = ctk.CTkLabel(
                left_frame,
                text="",
                image=warehouse_img
            )
            self.image_label.grid(row=0, column=0, sticky="nsew")

            # Bind resize event to update image size
            def update_image_size(event=None):
                new_width = self.winfo_width() // 2
                new_height = self.winfo_height()
                warehouse_img.configure(size=(new_width, new_height))
            
            self.bind('<Configure>', update_image_size)
        except:
            # Fallback if image not found
            self.image_label = ctk.CTkLabel(
                left_frame,
                text="Warehouse\nManagement\nSystem",
                font=("Helvetica", 24, "bold"),
                justify="center"
            )
            self.image_label.grid(row=0, column=0, sticky="nsew")

        # Right side - Registration Form
        current_row = 0
        
        # Logo
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open(relative_to_assets("logo.png")),
                size=(50, 50)
            )
            self.logo_label = ctk.CTkLabel(
                right_frame,
                text="",
                image=logo_img,
                anchor="w"
            )
            self.logo_label.grid(row=current_row, column=0, sticky="w", padx=(50, 20), pady=(20, 0))
            current_row += 1
        except:
            current_row = 0

        # Create a frame for the registration form
        register_form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        register_form_frame.grid(row=current_row, column=0, sticky="w", padx=(50, 20))
        register_form_frame.grid_columnconfigure(0, weight=1)

        form_row = 0

        # Welcome Text
        self.welcome_label = ctk.CTkLabel(
            register_form_frame,
            text="Đăng ký tài khoản",
            font=("Helvetica", 32, "bold"),
            text_color="#16141B",
            anchor="w"
        )
        self.welcome_label.grid(row=form_row, column=0, sticky="w", pady=(0, 20))
        form_row += 1

        # Username field
        self.username_label = ctk.CTkLabel(
            register_form_frame,
            text="Tên đăng nhập",
            font=("Helvetica", 12),
            text_color="#006EC4",
            anchor="w"
        )
        self.username_label.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        self.username_entry = ctk.CTkEntry(
            register_form_frame,
            width=350,
            height=40,
            placeholder_text="Nhập tên đăng nhập",
            border_width=1,
            corner_radius=8
        )
        self.username_entry.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        # Full Name field (formerly Email field)
        self.fullName_label = ctk.CTkLabel(
            register_form_frame,
            text="Họ và tên",
            font=("Helvetica", 12),
            text_color="#006EC4",
            anchor="w"
        )
        self.fullName_label.grid(row=form_row, column=0, sticky="w", pady=(10, 0))
        form_row += 1

        self.fullName_entry = ctk.CTkEntry(
            register_form_frame,
            width=350,
            height=40,
            placeholder_text="Nhập họ và tên",
            border_width=1,
            corner_radius=8
        )
        self.fullName_entry.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        # Password field
        self.password_label = ctk.CTkLabel(
            register_form_frame,
            text="Mật khẩu",
            font=("Helvetica", 12),
            text_color="#006EC4",
            anchor="w"
        )
        self.password_label.grid(row=form_row, column=0, sticky="w", pady=(10, 0))
        form_row += 1

        self.password_entry = ctk.CTkEntry(
            register_form_frame,
            width=350,
            height=40,
            placeholder_text="Nhập mật khẩu",
            border_width=1,
            corner_radius=8,
            show="•"
        )
        self.password_entry.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        # Confirm Password field
        self.confirm_password_label = ctk.CTkLabel(
            register_form_frame,
            text="Xác nhận mật khẩu",
            font=("Helvetica", 12),
            text_color="#006EC4",
            anchor="w"
        )
        self.confirm_password_label.grid(row=form_row, column=0, sticky="w", pady=(10, 0))
        form_row += 1

        self.confirm_password_entry = ctk.CTkEntry(
            register_form_frame,
            width=350,
            height=40,
            placeholder_text="Nhập lại mật khẩu",
            border_width=1,
            corner_radius=8,
            show="•"
        )
        self.confirm_password_entry.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        # Register Button
        self.register_button = ctk.CTkButton(
            register_form_frame,
            text="Đăng ký",
            font=("Helvetica", 14, "bold"),
            width=350,
            height=40,
            corner_radius=8,
            command=self._on_register_click
        )
        self.register_button.grid(row=form_row, column=0, sticky="w", pady=(20, 0))
        form_row += 1

        # Login Link
        self.login_button = ctk.CTkButton(
            register_form_frame,
            text="Đã có tài khoản? Đăng nhập",
            font=("Helvetica", 14),
            width=350,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            text_color="#006EC4",
            hover_color="#F0F0F0",
            command=self._on_login_click
        )
        self.login_button.grid(row=form_row, column=0, sticky="w", pady=(5, 0))

    def _on_register_click(self):
        ten_dang_nhap = self.username_entry.get()
        ho_ten = self.fullName_entry.get()
        mat_khau = self.password_entry.get()
        xac_nhan_mat_khau = self.confirm_password_entry.get()

        if not all([ten_dang_nhap, ho_ten, mat_khau, xac_nhan_mat_khau]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return

        if mat_khau != xac_nhan_mat_khau:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp")
            return

        success, message = self._controller.dangKy(ten_dang_nhap, mat_khau, ho_ten)
        if success:
            messagebox.showinfo("Thành công", message)
            self._on_login_click()
        else:
            messagebox.showerror("Lỗi", message)

    def _on_login_click(self):
        from app.views.login_view import LoginView
        self.destroy()
        LoginView(self.parent)
