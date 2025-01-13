from pathlib import Path
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from app.controllers.user_controller import UserController
from app.views.admin.admin_dashboard import AdminDashboard
from app.views.user.user_dashboard import UserDashboard
from app.views.manager.manager_dashboard import ManagerDashboard
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent.parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class LoginView(ctk.CTkFrame):
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
        self.grid_columnconfigure(0, weight=1)  # Left side - exactly half
        self.grid_columnconfigure(1, weight=1)  # Right side - exactly half
        self.grid_rowconfigure(0, weight=1)
        
        # Create left and right frames
        left_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)
        
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

        # Right side - Login Form
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

        # Create a frame for the login form
        login_form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        login_form_frame.grid(row=current_row, column=0, sticky="w", padx=(50, 20))
        login_form_frame.grid_columnconfigure(0, weight=1)

        form_row = 0

        # Welcome Text
        self.welcome_label = ctk.CTkLabel(
            login_form_frame,
            text="Welcome ",
            font=("Helvetica", 32, "bold"),
            text_color="#16141B",
            anchor="w"
        )
        self.welcome_label.grid(row=form_row, column=0, sticky="w", pady=(0, 20))
        form_row += 1

        # Login Form
        self.email_label = ctk.CTkLabel(
            login_form_frame,
            text="Email",
            font=("Helvetica", 12),
            text_color="#006EC4",
            anchor="w"
        )
        self.email_label.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        self.email_entry = ctk.CTkEntry(
            login_form_frame,
            width=350,
            height=40,
            placeholder_text="Nh\u1eadp email",
            border_width=1,
            corner_radius=8
        )
        self.email_entry.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        self.password_label = ctk.CTkLabel(
            login_form_frame,
            text="Password",
            font=("Helvetica", 12),
            text_color="#006EC4",
            anchor="w"
        )
        self.password_label.grid(row=form_row, column=0, sticky="w", pady=(10, 0))
        form_row += 1

        self.password_entry = ctk.CTkEntry(
            login_form_frame,
            width=350,
            height=40,
            placeholder_text="Nh\u1eadp m\u1eadt kh\u1ea9u",
            border_width=1,
            corner_radius=8,
            show="\u2022"
        )
        self.password_entry.grid(row=form_row, column=0, sticky="w")
        form_row += 1

        # Login Button
        self.login_button = ctk.CTkButton(
            login_form_frame,
            text="Đăng nhập",
            font=("Helvetica", 14, "bold"),
            width=350,
            height=40,
            corner_radius=8,
            command=self._on_login_click
        )
        self.login_button.grid(row=form_row, column=0, sticky="w", pady=(10, 0))
        form_row += 1

        # Register Link
        self.register_button = ctk.CTkButton(
            login_form_frame,
            text="Đăng ký",
            font=("Helvetica", 14),
            width=350,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            text_color="#006EC4",
            hover_color="#F0F0F0",
            command=self._on_register_click
        )
        self.register_button.grid(row=form_row, column=0, sticky="w", pady=(5, 0))

    def _on_login_click(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        success, user_data = self._controller.login(email, password)

        
        if success:
            if user_data['role_name'] == "registered_user":
                messagebox.showerror("Notice", "Tài khoản cần được phê duyệt để có thể vào ứng dụng!")
                return
            # First destroy the login view
            self.destroy()
            # Then destroy the parent window if it exists
            if hasattr(self, 'parent') and self.parent:
                self.parent.destroy()
            
            # Create the appropriate dashboard or show notice
            if user_data['role_name'] == "administrator":
                app = AdminDashboard(user_data=user_data)
                app.mainloop()
            elif user_data['role_name'] == "manager":
                app = ManagerDashboard(user_data=user_data)
                app.mainloop()
            else:
                app = UserDashboard(user_data=user_data)
                app.mainloop()
        else:
            messagebox.showerror("Error", user_data)  # Show error message

    def _on_register_click(self):
        from app.views.register_view import RegisterView
        self.destroy()
        RegisterView(self.parent)
