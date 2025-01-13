import customtkinter as ctk
from app.controllers.user_controller import UserController
from PIL import Image
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

class UsersPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = UserController()
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0
        self.search_query = ""
        
        # Load icons
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        self.search_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'search.png')),
            size=(20, 20)
        )
        self.plus_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'plus.png')),
            size=(20, 20)
        )
        self.trash_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'trash.png')),
            size=(16, 16)
        )
        self.edit_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'edit.png')),
            size=(16, 16)
        )
        self.chevron_left_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-left.png')),
            size=(20, 20)
        )
        self.chevron_right_image = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'chevron-right.png')),
            size=(20, 20)
        )
        self.filter_icon = ctk.CTkImage(
            light_image=Image.open(str(assets_path / 'filter.png')),
            size=(20, 20)
        )
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create top section with search and buttons
        top_section = ctk.CTkFrame(self, fg_color="transparent")
        top_section.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 20))
        top_section.grid_columnconfigure(1, weight=1)
        
        # Create search frame
        search_frame = ctk.CTkFrame(
            top_section,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        search_frame.grid(row=0, column=0, sticky="w")
        
        # Add search icon and entry
        search_icon_label = ctk.CTkLabel(
            search_frame,
            text="",
            image=self.search_icon
        )
        search_icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search users...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        self.search_entry.bind("<Return>", self.on_search)
        
        # Create buttons container
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add filter button
        filter_button = ctk.CTkButton(
            buttons_frame,
            text="Filter",
            image=self.filter_icon,
            compound="left",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=45,
            corner_radius=8,
            command=self.show_filter_dialog  # This should be a method to handle filter actions
        )
        filter_button.pack(side="left", padx=(0, 10))
        
        # Create table container
        table_container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="#F0F0F0"
        )
        table_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        # Create scrollable frame for table
        self.table_frame = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent"
        )
        self.table_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        # Define column configurations
        self.columns = [
            {"name": "Username", "key": "username", "width": 100},
            {"name": "Email", "key": "email", "width": 150},
            {"name": "Role", "key": "role_name", "width": 100},
            {"name": "Approved", "key": "is_approved", "width": 100},
            {"name": "Actions", "key": "actions", "width": 100}
        ]
        
        # Create table header
        header_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="#F8F9FA",
            height=50
        )
        header_frame.pack(fill="x", expand=True)
        header_frame.pack_propagate(False)
        
        # Add header labels
        for i, col in enumerate(self.columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col["name"],
                font=("", 13, "bold"),
                text_color="#16151C",
                anchor="w",
                width=col["width"]
            )
            label.grid(row=0, column=i, padx=(20 if i == 0 else 10, 10), pady=15, sticky="w")
            
        # Create frame for table content
        self.content_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True)
        
        # Load initial data
        self.load_users()
    
    def on_search(self, event=None):
        """Handle search when Enter is pressed"""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1  # Reset to first page
        self.load_users()

    def load_users(self):
        """Load users into the table"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Calculate pagination
        offset = (self.current_page - 1) * self.items_per_page
        
        # Get users from controller with pagination
        users, total_count = self.controller.get_users_paginated(
            offset=offset,
            limit=self.items_per_page,
            search_query=self.search_query
        )
        
        self.total_items = total_count
        total_pages = -(-total_count // self.items_per_page)  # Ceiling division
        
        # Configure grid columns for content frame
        self.content_frame.grid_columnconfigure(tuple(range(len(self.columns))), weight=1)
        
        # Create rows for each user
        for i, user in enumerate(users):
            row_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color="white" if i % 2 == 0 else "#F8F9FA",
                height=50
            )
            row_frame.pack(fill="x")
            
            # Add user data
            for j, col in enumerate(self.columns):
                if col["key"] == "actions":
                    # Skip action buttons for admin accounts
                    if user['role_name'].lower() == 'administrator':
                        continue

                    # Create actions frame
                    actions_frame = ctk.CTkFrame(
                        row_frame,
                        fg_color="transparent"
                    )
                    actions_frame.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
                    
                    if user['is_approved']:
                        # Set Role button with edit icon
                        set_role_btn = ctk.CTkButton(
                            actions_frame,
                            text="",  # No text, only icon
                            image=self.edit_icon,
                            width=30,  # Adjust width to fit icon
                            height=30,
                            fg_color="#006EC4",
                            hover_color="#0059A1",
                            command=lambda u=user: self.set_role(u)
                        )
                        set_role_btn.pack(side="left", padx=(0, 5))
                        
                        # Delete button with trash icon
                        delete_btn = ctk.CTkButton(
                            actions_frame,
                            text="",  # No text, only icon
                            image=self.trash_icon,
                            width=30,  # Adjust width to fit icon
                            height=30,
                            fg_color="#e03137",
                            hover_color="#b32429",
                            command=lambda u=user: self.delete_user(u)
                        )
                        delete_btn.pack(side="left")
                    else:
                        # Approve button
                        approve_btn = ctk.CTkButton(
                            actions_frame,
                            text="Approve",
                            width=60,
                            height=30,
                            fg_color="#006EC4",
                            text_color="white",
                            hover_color="#0059A1",
                            command=lambda u=user: self.approve_user(u)
                        )
                        approve_btn.pack(side="left", padx=(0, 5))
                        
                        # Reject button
                        reject_btn = ctk.CTkButton(
                            actions_frame,
                            text="Reject",
                            width=60,
                            height=30,
                            fg_color="#e03137",
                            text_color="white",
                            hover_color="#b32429",
                            command=lambda u=user: self.reject_user(u)
                        )
                        reject_btn.pack(side="left")
                    
                else:
                    # Regular text columns
                    value = str(user.get(col["key"], "") or "")
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        anchor="w",
                        width=col["width"]
                    )
                    label.grid(row=0, column=j, padx=(20 if j == 0 else 10, 10), pady=10, sticky="w")
            
            # Add separator
            separator = ctk.CTkFrame(
                self.content_frame,
                fg_color="#E5E5E5",
                height=1
            )
            separator.pack(fill="x")

        # Add pagination controls at the bottom
        self.create_pagination_controls(total_pages)

    def create_pagination_controls(self, total_pages):
        """Create pagination controls"""
        # Create or clear pagination frame
        if hasattr(self, 'pagination_frame'):
            for widget in self.pagination_frame.winfo_children():
                widget.destroy()
        else:
            self.pagination_frame = ctk.CTkFrame(self, fg_color="white", height=60)
            self.pagination_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
            self.pagination_frame.grid_propagate(False)
        
        # Create container for pagination elements
        controls_frame = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
        controls_frame.pack(expand=True, fill="both")
        
        # Left side - showing entries info
        left_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=20)
        
        start_index = (self.current_page - 1) * self.items_per_page + 1
        end_index = min(start_index + self.items_per_page - 1, self.total_items)
        
        showing_label = ctk.CTkLabel(
            left_frame,
            text=f"Showing {start_index}-{end_index} of {self.total_items} entries",
            text_color="#6F6E77"
        )
        showing_label.pack(side="left")
        
        # Right side - pagination buttons
        right_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=20)
        
        # Previous page button
        prev_button = ctk.CTkButton(
            right_frame,
            text="",
            image=self.chevron_left_image,
            width=30,
            height=30,
            fg_color="#F8F9FA" if self.current_page > 1 else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.previous_page if self.current_page > 1 else None
        )
        prev_button.pack(side="left", padx=(0, 5))
        
        # Page number buttons
        visible_pages = 5
        start_page = max(1, min(self.current_page - visible_pages // 2,
                               total_pages - visible_pages + 1))
        end_page = min(start_page + visible_pages - 1, total_pages)
        
        for page in range(start_page, end_page + 1):
            is_current = page == self.current_page
            page_button = ctk.CTkButton(
                right_frame,
                text=str(page),
                width=30,
                height=30,
                fg_color="#006EC4" if is_current else "#F8F9FA",
                text_color="white" if is_current else "#16151C",
                hover_color="#0059A1" if is_current else "#E8E9EA",
                command=lambda p=page: self.go_to_page(p)
            )
            page_button.pack(side="left", padx=2)
        
        # Next page button
        next_button = ctk.CTkButton(
            right_frame,
            text="",
            image=self.chevron_right_image,
            width=30,
            height=30,
            fg_color="#F8F9FA" if self.current_page < total_pages else "#E9ECEF",
            text_color="#16151C",
            hover_color="#E8E9EA",
            command=self.next_page if self.current_page < total_pages else None
        )
        next_button.pack(side="left", padx=(5, 0))

    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_users()

    def next_page(self):
        """Go to next page"""
        self.current_page += 1
        self.load_users()

    def go_to_page(self, page):
        """Go to specific page"""
        self.current_page = page
        self.load_users()

    def approve_user(self, user):
        """Approve a user"""
        if self.controller.approve_user(user["user_id"]):
            self.load_users()  # Refresh the list

    def reject_user(self, user):
        """Reject a user"""
        if self.controller.reject_user(user["user_id"]):
            self.load_users()  # Refresh the list

    def show_filter_dialog(self):
        """Show filter options dialog"""
        # Implement the logic to show a filter dialog or apply filters
        print("Filter dialog opened")

    def set_role(self, user):
        """Open a dialog to set the user's role"""
        # Create a new dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("Set Role")
        dialog.geometry("300x200")  # Adjusted height to accommodate additional label
        
        # Display the current role
        current_role_label = ctk.CTkLabel(dialog, text=f"Current Role: {user.get('role_name', 'Unknown')}")
        current_role_label.pack(pady=10)
        
        # Add a label for role selection
        label = ctk.CTkLabel(dialog, text="Select a new role for the user:")
        label.pack(pady=10)
        
        # Initialize role_var with the user's current role
        current_role = user.get("role_name", "user")  # Fetch the current role from the user data
        role_var = ctk.StringVar(value=current_role)  # Set initial value to current role
        
        # Create a frame to hold the radio buttons with a transparent background
        radio_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        radio_frame.pack(pady=10)
        
        # Create radio buttons for each role
        user_radio = ctk.CTkRadioButton(radio_frame, text="User", variable=role_var, value="user")
        manager_radio = ctk.CTkRadioButton(radio_frame, text="Manager", variable=role_var, value="manager")
        
        # Pack the radio buttons horizontally
        user_radio.pack(side="left", padx=10)
        manager_radio.pack(side="left", padx=10)
        
        # Add a button to confirm the role change
        confirm_button = ctk.CTkButton(
            dialog,
            text="Confirm",
            command=lambda: self.confirm_role_change(user, role_var.get(), dialog)
        )
        confirm_button.pack(pady=10)

    def confirm_role_change(self, user, new_role, dialog):
        """Confirm the role change and update the user"""
        if self.controller.set_user_role(user["user_id"], new_role):
            self.load_users()  # Refresh the list to show updated role
            dialog.destroy()
            # Show a success message using tkinter
            tk.messagebox.showinfo("Success", "User role updated successfully.")
        else:
            # Show an error message using tkinter
            tk.messagebox.showerror("Error", "Failed to update user role.")
