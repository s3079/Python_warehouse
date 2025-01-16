import customtkinter as ctk

class CategoryDialog(ctk.CTkToplevel):
    def __init__(self, parent, category=None, on_save=None):
        super().__init__(parent)
        
        # Set up the dialog window
        self.title("Add Category" if not category else "Edit Category")
        self.geometry("500x380")
        self.resizable(False, False)
        
        # Store callback and category
        self.on_save = on_save
        self.category = category
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Create main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Add header
        header_text = "Add New Category" if not category else "Edit Category"
        header = ctk.CTkLabel(
            main_container,
            text=header_text,
            font=("", 20, "bold"),
            text_color="#16151C"
        )
        header.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # Add form fields
        # Name field
        name_label = ctk.CTkLabel(
            main_container,
            text="Name",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        name_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            main_container,
            placeholder_text="Enter category name",
            height=40,
            font=("", 13),
            corner_radius=8
        )
        self.name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # Description field
        description_label = ctk.CTkLabel(
            main_container,
            text="Description",
            font=("", 13, "bold"),
            text_color="#16151C"
        )
        description_label.grid(row=3, column=0, sticky="w", pady=(0, 5))
        
        self.description_text = ctk.CTkTextbox(
            main_container,
            height=120,
            font=("", 13),
            corner_radius=8,
            wrap="word"
        )
        self.description_text.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        
        # Add buttons container
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            height=45,
            corner_radius=8,
            command=self.destroy
        )
        cancel_button.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Save button
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Save Category",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            height=45,
            corner_radius=8,
            command=self.save_category
        )
        save_button.grid(row=0, column=1, sticky="w")
        
        # If editing, populate fields with existing data
        if category:
            self.name_entry.insert(0, category["ten"])
            if category["mo_ta"]:
                self.description_text.insert("1.0", category["mo_ta"])
        
        # Focus on name entry
        self.name_entry.focus_set()
    
    def save_category(self):
        """Validate and save category data"""
        name = self.name_entry.get().strip()
        description = self.description_text.get("1.0", "end-1c").strip()
        
        # Validate name
        if not name:
            self.show_error("Name is required")
            return
        
        # Prepare category data
        category_data = {
            "ten": name,
            "mo_ta": description
        }
        
        # If editing, include category_id
        if self.category:
            category_data["ma_danh_muc"] = self.category["ma_danh_muc"]
        
        # Call save callback
        if self.on_save:
            try:
                self.on_save(category_data)
                self.destroy()
            except Exception as e:
                self.show_error(str(e))
    
    def show_error(self, message):
        """Show error message in a dialog"""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x150")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        # Center the error dialog
        error_dialog.grid_columnconfigure(0, weight=1)
        error_dialog.grid_rowconfigure(0, weight=1)
        
        # Add error message
        message_label = ctk.CTkLabel(
            error_dialog,
            text=message,
            font=("", 13),
            text_color="#FF4842",
            wraplength=250
        )
        message_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Add OK button
        ok_button = ctk.CTkButton(
            error_dialog,
            text="OK",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            height=35,
            corner_radius=8,
            command=error_dialog.destroy
        )
        ok_button.grid(row=1, column=0, pady=(0, 20))
