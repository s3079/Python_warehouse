import tkinter as tk
from tkinter import ttk, messagebox

class UserDialog:
    def __init__(self, parent, title, initial_data=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        window_width = 400
        window_height = 300
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar(value=initial_data['username'] if initial_data else "")
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Email
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar(value=initial_data['email'] if initial_data else "")
        self.email_entry = ttk.Entry(main_frame, textvariable=self.email_var)
        self.email_entry.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Role
        ttk.Label(main_frame, text="Role:").grid(row=3, column=0, sticky="w", pady=5)
        self.role_var = tk.StringVar(value=initial_data['role'] if initial_data else "user")
        role_frame = ttk.Frame(main_frame)
        role_frame.grid(row=3, column=1, sticky="ew", pady=5)
        
        ttk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="admin").pack(side=tk.LEFT)
        ttk.Radiobutton(role_frame, text="User", variable=self.role_var, value="user").pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        
        # Make dialog modal
        self.dialog.wait_window()
    
    def _on_ok(self):
        """Handle OK button click"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        email = self.email_var.get().strip()
        role = self.role_var.get()
        
        if not username:
            messagebox.showerror("Error", "Username is required")
            return
        
        if not email:
            messagebox.showerror("Error", "Email is required")
            return
        
        if not password and not hasattr(self, 'editing'):
            messagebox.showerror("Error", "Password is required for new users")
            return
        
        self.result = {
            'username': username,
            'password': password,
            'email': email,
            'role': role
        }
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button click"""
        self.dialog.destroy()
