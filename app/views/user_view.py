import tkinter as tk
from tkinter import ttk, messagebox
from app.views.base_view import BaseView
from app.controllers.user_controller import UserController

class UserView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self._controller = UserController()
        self._current_frame = None
        self.show_login()

    def show_login(self):
        """Show login form"""
        if self._current_frame:
            self._current_frame.destroy()

        self._current_frame = ttk.Frame(self)
        self._current_frame.grid(row=0, column=0, padx=20, pady=20)

        # Title
        title_label = ttk.Label(self._current_frame, text="Login", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        ttk.Label(self._current_frame, text="Username:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = ttk.Entry(self._current_frame)
        username_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        # Password
        ttk.Label(self._current_frame, text="Password:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = ttk.Entry(self._current_frame, show="*")
        password_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        # Login button
        login_btn = ttk.Button(self._current_frame, text="Login",
                             command=lambda: self._process_login(username_entry.get(), password_entry.get()))
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Register link
        register_link = ttk.Button(self._current_frame, text="Don't have an account? Register",
                                 command=self.show_register)
        register_link.grid(row=4, column=0, columnspan=2)

    def show_register(self):
        """Show registration form"""
        if self._current_frame:
            self._current_frame.destroy()

        self._current_frame = ttk.Frame(self)
        self._current_frame.grid(row=0, column=0, padx=20, pady=20)

        # Title
        title_label = ttk.Label(self._current_frame, text="Register", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        ttk.Label(self._current_frame, text="Username:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = ttk.Entry(self._current_frame)
        username_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        # Email
        ttk.Label(self._current_frame, text="Email:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        email_entry = ttk.Entry(self._current_frame)
        email_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        # Password
        ttk.Label(self._current_frame, text="Password:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        password_entry = ttk.Entry(self._current_frame, show="*")
        password_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        # Confirm Password
        ttk.Label(self._current_frame, text="Confirm Password:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        confirm_password_entry = ttk.Entry(self._current_frame, show="*")
        confirm_password_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        # Register button
        register_btn = ttk.Button(self._current_frame, text="Register",
                                command=lambda: self._process_register(
                                    username_entry.get(),
                                    email_entry.get(),
                                    password_entry.get(),
                                    confirm_password_entry.get()))
        register_btn.grid(row=5, column=0, columnspan=2, pady=20)

        # Login link
        login_link = ttk.Button(self._current_frame, text="Already have an account? Login",
                              command=self.show_login)
        login_link.grid(row=6, column=0, columnspan=2)

    def _process_login(self, username, password):
        """Process login form submission"""
        if not username or not password:
            self.show_error("Please fill in all fields")
            return

        success, result = self._controller.login(username, password)
        if success:
            self.show_success("Login successful!")
            # Here you would typically store the user session and redirect to main app
            print("User logged in:", result)
        else:
            self.show_error(result)

    def _process_register(self, username, email, password, confirm_password):
        """Process registration form submission"""
        if not username or not email or not password or not confirm_password:
            self.show_error("Please fill in all fields")
            return

        if password != confirm_password:
            self.show_error("Passwords do not match")
            return

        success, message = self._controller.register(username, password, email)
        if success:
            self.show_success(message)
            self.show_login()  # Redirect to login page
        else:
            self.show_error(message)
