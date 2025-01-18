import customtkinter as ctk
from app.views.dialogs.center_dialog import CenterDialog
from app.controllers.user_controller import UserController

class UserDialog(CenterDialog):
    def __init__(self, parent, user=None):
        self.controller = UserController()
        self.user = user
        title = "Sửa người dùng" if user else "Thêm người dùng"
        super().__init__(parent, title, "500x400")
        
        self.tao_giao_dien()
        if user:
            self.tai_du_lieu_nguoi_dung()

    def tao_giao_dien(self):
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="Tên đăng nhập:",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10,5))
        
        self.username_entry = ctk.CTkEntry(content_frame)
        self.username_entry.pack(fill="x", padx=10, pady=(0,10))
        
        ctk.CTkLabel(
            content_frame,
            text="Email:",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10,5))
        
        self.email_entry = ctk.CTkEntry(content_frame)
        self.email_entry.pack(fill="x", padx=10, pady=(0,10))
        
        if not self.user:
            ctk.CTkLabel(
                content_frame,
                text="Mật khẩu:",
                anchor="w"
            ).pack(fill="x", padx=10, pady=(10,5))
            
            self.password_entry = ctk.CTkEntry(content_frame, show="*")
            self.password_entry.pack(fill="x", padx=10, pady=(0,10))
        
        ctk.CTkLabel(
            content_frame,
            text="Vai trò:",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10,5))
        
        self.roles = self.controller.lay_danh_sach_vai_tro()
        role_names = [role["role_name"] for role in self.roles]
        
        self.role_var = ctk.StringVar()
        self.role_dropdown = ctk.CTkOptionMenu(
            content_frame,
            values=role_names,
            variable=self.role_var
        )
        self.role_dropdown.pack(fill="x", padx=10, pady=(0,10))
        
        if self.user:
            ctk.CTkLabel(
                content_frame,
                text="Trạng thái:",
                anchor="w"
            ).pack(fill="x", padx=10, pady=(10,5))
            
            self.status_var = ctk.BooleanVar()
            self.status_switch = ctk.CTkSwitch(
                content_frame,
                text="Đã duyệt",
                variable=self.status_var
            )
            self.status_switch.pack(fill="x", padx=10, pady=(0,10))
        
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(20,10))
        
        ctk.CTkButton(
            button_frame,
            text="Hủy",
            command=self.destroy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Lưu",
            command=self.luu_nguoi_dung
        ).pack(side="left", padx=5)

    def tai_du_lieu_nguoi_dung(self):
        self.username_entry.insert(0, self.user["username"])
        self.email_entry.insert(0, self.user["email"])
        self.role_var.set(self.user["role_name"])
        if hasattr(self, "status_var"):
            self.status_var.set(self.user["is_approved"])

    def luu_nguoi_dung(self):
        data = {
            "username": self.username_entry.get(),
            "email": self.email_entry.get(),
            "role_id": next(role["role_id"] for role in self.roles 
                          if role["role_name"] == self.role_var.get())
        }
        
        if not self.user:
            data["password"] = self.password_entry.get()
            result = self.controller.tao_nguoi_dung(data)
        else:
            data["is_approved"] = self.status_var.get()
            result = self.controller.cap_nhat_nguoi_dung(self.user["user_id"], data)
        
        if result:
            self.destroy()
