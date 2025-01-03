import tkinter as tk
from tkinter import ttk

class CategoryDialog:
    def __init__(self, parent, title, initial_data=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        window_width = 400
        window_height = 200
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar(value=initial_data['name'] if initial_data else "")
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_var = tk.StringVar(value=initial_data['description'] if initial_data else "")
        self.desc_entry = ttk.Entry(main_frame, textvariable=self.desc_var)
        self.desc_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        
        # Make dialog modal
        self.dialog.wait_window()
    
    def _on_ok(self):
        """Handle OK button click"""
        name = self.name_var.get().strip()
        description = self.desc_var.get().strip()
        
        if not name:
            tk.messagebox.showerror("Error", "Name is required")
            return
        
        self.result = {
            'name': name,
            'description': description
        }
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button click"""
        self.dialog.destroy()
