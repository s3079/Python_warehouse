import customtkinter as ctk
from app.views.admin.dialogs.center_dialog import CenterDialog
from app.controllers.user_controller import UserController

class UserDialog(CenterDialog):
    def __init__(self, parent, user=None):
        self.controller = UserController()
        self.user = user
        title = "Edit User" if user else "Add User"
        super().__init__(parent, title, "500x400")
        
        self.setup_ui()
        if user:
            self.load_user_data()

    def setup_ui(self):
        # Main content frame
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Username
        ctk.CTkLabel(
            content_frame,
            text="Username:",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10,5))
        
        self.username_entry = ctk.CTkEntry(content_frame)
        self.username_entry.pack(fill="x", padx=10, pady=(0,10))
        
        # Email
        ctk.CTkLabel(
            content_frame,
            text="Email:",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10,5))
        
        self.email_entry = ctk.CTkEntry(content_frame)
        self.email_entry.pack(fill="x", padx=10, pady=(0,10))
        
        # Password (only for new users)
        if not self.user:
            ctk.CTkLabel(
                content_frame,
                text="Password:",
                anchor="w"
            ).pack(fill="x", padx=10, pady=(10,5))
            
            self.password_entry = ctk.CTkEntry(content_frame, show="*")
            self.password_entry.pack(fill="x", padx=10, pady=(0,10))
        
        # Role selection
        ctk.CTkLabel(
            content_frame,
            text="Role:",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10,5))
        
        self.roles = self.controller.get_roles()
        role_names = [role["role_name"] for role in self.roles]
        
        self.role_var = ctk.StringVar()
        self.role_dropdown = ctk.CTkOptionMenu(
            content_frame,
            values=role_names,
            variable=self.role_var
        )
        self.role_dropdown.pack(fill="x", padx=10, pady=(0,10))
        
        # Approval status (only for editing)
        if self.user:
            ctk.CTkLabel(
                content_frame,
                text="Status:",
                anchor="w"
            ).pack(fill="x", padx=10, pady=(10,5))
            
            self.status_var = ctk.BooleanVar()
            self.status_switch = ctk.CTkSwitch(
                content_frame,
                text="Approved",
                variable=self.status_var
            )
            self.status_switch.pack(fill="x", padx=10, pady=(0,10))
        
        # Buttons frame
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(20,10))
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save_user
        ).pack(side="left", padx=5)

    def load_user_data(self):
        self.username_entry.insert(0, self.user["username"])
        self.email_entry.insert(0, self.user["email"])
        self.role_var.set(self.user["role_name"])
        if hasattr(self, "status_var"):
            self.status_var.set(self.user["is_approved"])

    def save_user(self):
        data = {
            "username": self.username_entry.get(),
            "email": self.email_entry.get(),
            "role_id": next(role["role_id"] for role in self.roles 
                          if role["role_name"] == self.role_var.get())
        }
        
        if not self.user:  # New user
            data["password"] = self.password_entry.get()
            result = self.controller.create_user(data)
        else:  # Edit user
            data["is_approved"] = self.status_var.get()
            result = self.controller.update_user(self.user["user_id"], data)
        
        if result:
            self.destroy()
