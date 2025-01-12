import customtkinter as ctk

class CenterDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, size="400x200"):
        super().__init__(parent)
        self.title(title)
        self.geometry(size)
        self.resizable(False, False)
        self.transient(parent)  # Set the main window as parent
        self.grab_set()
        self.focus_set()  # Give focus to the dialog
        
        # Center the dialog
        self.center_dialog()
    
    def center_dialog(self):
        """Center dialog window relative to its parent window"""
        def _center():
            self.update_idletasks()
            
            # Get dialog dimensions
            dialog_width = self.winfo_width()
            dialog_height = self.winfo_height()
            
            # Get parent window position and dimensions
            parent_x = self.master.winfo_rootx()
            parent_y = self.master.winfo_rooty()
            parent_width = self.master.winfo_width()
            parent_height = self.master.winfo_height()
            
            # Calculate position
            x = parent_x + (parent_width - dialog_width) // 2
            y = parent_y + (parent_height - dialog_height) // 2
            
            # Set dialog position
            self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Schedule centering after the dialog is rendered
        self.after(10, _center) 