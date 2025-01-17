import customtkinter as ctk
from app.views.admin.dialogs.center_dialog import CenterDialog

class DeleteDialog(CenterDialog):
    def __init__(self, parent, item_name, on_confirm=None):
        super().__init__(parent, "Delete Confirmation", "400x250")
        
        self.on_confirm = on_confirm
        
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
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
            text=f"Bạn có chắc chắn muốn xóa '{item_name}'?\nHành động này không thể hoàn tác.",
            font=("", 13),
            text_color="#16151C"
        )
        message_label.pack(pady=(0, 20))
        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
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
            command=self.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Xóa",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=self.xac_nhan
        )
        delete_button.pack(side="right")

    def xac_nhan(self):
        if self.on_confirm:
            self.on_confirm()
        self.destroy() 