import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path
from app.controllers.category_controller import CategoryController
from app.views.admin.dialogs.category_dialog import CategoryDialog
import math
import tkinter as tk

class CategoriesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = CategoryController()
        self.current_page = 1
        self.items_per_page = 10
        self.total_items = 0
        self.search_query = ""  # Add search query variable
        
        # Load icons
        assets_path = Path(__file__).parent.parent.parent / 'assets' / 'icons'
        search_icon_path = str(assets_path / 'search.png')
        trash_icon_path = str(assets_path / 'trash.png')
        edit_icon_path = str(assets_path / 'edit.png')
        plus_icon_path = str(assets_path / 'plus.png')
        filter_icon_path = str(assets_path / 'filter.png')
        chevron_left_path = str(assets_path / 'chevron-left.png')
        chevron_right_path = str(assets_path / 'chevron-right.png')
        
        # Create all icons
        self.search_icon = ctk.CTkImage(
            light_image=Image.open(search_icon_path),
            dark_image=Image.open(search_icon_path),
            size=(20, 20)
        )
        
        self.filter_icon = ctk.CTkImage(
            light_image=Image.open(filter_icon_path),
            dark_image=Image.open(filter_icon_path),
            size=(20, 20)
        )
        
        self.plus_icon = ctk.CTkImage(
            light_image=Image.open(plus_icon_path),
            dark_image=Image.open(plus_icon_path),
            size=(20, 20)
        )
        
        self.trash_icon = ctk.CTkImage(
            light_image=Image.open(trash_icon_path),
            dark_image=Image.open(trash_icon_path),
            size=(16, 16)
        )
        
        self.edit_icon = ctk.CTkImage(
            light_image=Image.open(edit_icon_path),
            dark_image=Image.open(edit_icon_path),
            size=(16, 16)
        )
        
        self.chevron_left_image = ctk.CTkImage(
            light_image=Image.open(chevron_left_path),
            dark_image=Image.open(chevron_left_path),
            size=(20, 20)
        )
        
        self.chevron_right_image = ctk.CTkImage(
            light_image=Image.open(chevron_right_path),
            dark_image=Image.open(chevron_right_path),
            size=(20, 20)
        )
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create top section container
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
        
        # Add search icon
        search_icon_label = ctk.CTkLabel(
            search_frame,
            text="",
            image=self.search_icon
        )
        search_icon_label.pack(side="left", padx=(15, 5), pady=10)
        
        # Add search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search categories...",
            border_width=0,
            fg_color="transparent",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 15), pady=10)
        
        # Bind Enter key to search
        self.search_entry.bind("<Return>", self.on_search)
        
        # Create buttons container
        buttons_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Add new category button
        new_category_button = ctk.CTkButton(
            buttons_frame,
            text="Add Category",
            image=self.plus_icon,
            compound="left",  # Places the icon to the left of the text
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=140,  # Increased width to accommodate icon
            height=45,
            corner_radius=8,
            command=self.show_add_dialog
        )
        new_category_button.pack(side="left", padx=(0, 10))  # Added right padding
        
        # Add filter button
        filter_button = ctk.CTkButton(
            buttons_frame,
            text="",
            image=self.filter_icon,
            fg_color="transparent",
            text_color="#16151C",
            hover_color="#F0F0F0",
            width=45,
            height=45,
            corner_radius=8,
            command=self.show_filter_dialog
        )
        filter_button.pack(side="left")
        
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
        table_container.grid_rowconfigure(0, weight=1)  # Content area expands
        table_container.grid_rowconfigure(1, weight=0)  # Pagination stays at bottom

        # Create content area with fixed height for 10 rows
        content_frame = ctk.CTkFrame(
            table_container,
            fg_color="transparent",
            height=500  # Fixed height for 10 rows (10 * 50px)
        )
        content_frame.grid(row=0, column=0, sticky="nsew")
        content_frame.grid_propagate(False)  # Force fixed height
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Create scrollable frame inside content frame
        self.table_content = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="transparent",
            orientation="vertical"
        )
        self.table_content.grid(row=0, column=0, sticky="nsew")
        self.table_content.grid_columnconfigure(0, weight=1)

        # Create main frame to hold both header and content
        main_frame = ctk.CTkFrame(
            self.table_content,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True)
        
        # Set fixed minimum width for columns
        name_width = 200
        desc_width = 300
        total_width = 120
        actions_width = 80
        
        # Configure columns with weights and minimum sizes
        main_frame.grid_columnconfigure(0, weight=3, minsize=name_width)  # Name
        main_frame.grid_columnconfigure(1, weight=5, minsize=desc_width)  # Description
        main_frame.grid_columnconfigure(2, weight=2, minsize=total_width)  # Total Products
        main_frame.grid_columnconfigure(3, weight=1, minsize=actions_width)  # Actions
        
        # Create header row with fixed height
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#F8F9FA",
            height=50
        )
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=1)
        header_frame.grid_propagate(False)  # Force fixed height

        # Configure header columns with same weights and minimum sizes
        header_frame.grid_columnconfigure(0, weight=3, minsize=name_width)  # Name
        header_frame.grid_columnconfigure(1, weight=5, minsize=desc_width)  # Description
        header_frame.grid_columnconfigure(2, weight=2, minsize=total_width)  # Total Products
        header_frame.grid_columnconfigure(3, weight=1, minsize=actions_width)  # Actions
        header_frame.grid_propagate(False)

        # Add header labels with fixed widths
        name_header = ctk.CTkLabel(
            header_frame,
            text="Name",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=name_width
        )
        name_header.grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

        desc_header = ctk.CTkLabel(
            header_frame,
            text="Description",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=desc_width
        )
        desc_header.grid(row=0, column=1, padx=10, pady=15, sticky="w")

        total_header = ctk.CTkLabel(
            header_frame,
            text="Total Products",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=total_width
        )
        total_header.grid(row=0, column=2, padx=10, pady=15, sticky="w")

        actions_header = ctk.CTkLabel(
            header_frame,
            text="Actions",
            font=("", 13, "bold"),
            text_color="#16151C",
            anchor="w",
            width=actions_width
        )
        actions_header.grid(row=0, column=3, padx=10, pady=15, sticky="w")
        
        # Create content frame
        self.main_content = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        self.main_content.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        
        # Configure column weights for content
        self.main_content.grid_columnconfigure(0, weight=3, minsize=name_width)  # Name
        self.main_content.grid_columnconfigure(1, weight=5, minsize=desc_width)  # Description
        self.main_content.grid_columnconfigure(2, weight=2, minsize=total_width)  # Total Products
        self.main_content.grid_columnconfigure(3, weight=1, minsize=actions_width)  # Actions
        
        # Add pagination frame at the bottom with minimal height
        self.pagination_frame = ctk.CTkFrame(
            table_container,
            fg_color="#F8F9FA",
            height=50
        )
        self.pagination_frame.grid(row=1, column=0, sticky="ew")
        self.pagination_frame.grid_propagate(False)  # Force fixed height
        
        # Create pagination controls
        self.create_pagination_controls()
        
        # Load initial data
        self.load_categories()
    
    def create_pagination_controls(self):
        """Create pagination controls in the footer"""
        # Clear existing controls
        for widget in self.pagination_frame.winfo_children():
            widget.destroy()
            
        # Create left container for "Showing" dropdown
        left_container = ctk.CTkFrame(
            self.pagination_frame,
            fg_color="transparent"
        )
        left_container.pack(side="left", padx=20, pady=10)
        
        # Add "Showing" label
        showing_label = ctk.CTkLabel(
            left_container,
            text="Showing",
            font=("", 13),
            text_color="#6F6E77"
        )
        showing_label.pack(side="left", padx=(0, 10))
        
        # Add rows per page dropdown
        self.rows_per_page_var = ctk.StringVar(value=str(self.items_per_page))
        rows_dropdown = ctk.CTkOptionMenu(
            left_container,
            values=["10", "15", "20"],
            variable=self.rows_per_page_var,
            width=70,
            height=30,
            command=self.on_rows_per_page_change,
            fg_color="white",
            text_color="#16151C",
            button_color="#F0F0F0",
            button_hover_color="#E8E9EA",
            dropdown_fg_color="white",
            dropdown_hover_color="#F8F9FA",
            dropdown_text_color="#16151C"
        )
        rows_dropdown.pack(side="left")
        
        # Create right container for page navigation
        right_container = ctk.CTkFrame(
            self.pagination_frame,
            fg_color="transparent"
        )
        right_container.pack(side="right", padx=20, pady=10)
        
        # Previous page button
        self.prev_button = ctk.CTkButton(
            right_container,
            text="",
            image=self.chevron_left_image,
            fg_color="transparent",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=30,
            height=30,
            corner_radius=15,
            command=self.previous_page
        )
        self.prev_button.pack(side="left", padx=5)
        
        # Create page buttons container
        pages_container = ctk.CTkFrame(
            right_container,
            fg_color="transparent"
        )
        pages_container.pack(side="left", padx=10)
        
        # Calculate total pages and visible page numbers
        total_pages = math.ceil(self.total_items / self.items_per_page)
        visible_pages = self.get_visible_page_numbers(self.current_page, total_pages)
        
        # Add page buttons
        for page_num in visible_pages:
            if page_num == "...":
                # Ellipsis
                label = ctk.CTkLabel(
                    pages_container,
                    text="...",
                    font=("", 13),
                    text_color="#6F6E77",
                    width=30
                )
                label.pack(side="left", padx=2)
            else:
                # Page button
                is_current = page_num == self.current_page
                button = ctk.CTkButton(
                    pages_container,
                    text=str(page_num),
                    fg_color="#006EC4" if is_current else "transparent",
                    text_color="white" if is_current else "#16151C",
                    hover_color="#0059A1" if is_current else "#E8E9EA",
                    width=30,
                    height=30,
                    corner_radius=15,
                    command=lambda p=page_num: self.go_to_page(p)
                )
                button.pack(side="left", padx=2)
        
        # Next page button
        self.next_button = ctk.CTkButton(
            right_container,
            text="",
            image=self.chevron_right_image,
            fg_color="transparent",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=30,
            height=30,
            corner_radius=15,
            command=self.next_page
        )
        self.next_button.pack(side="left", padx=5)
        
        # Update button states
        self.update_pagination_buttons()
    
    def get_visible_page_numbers(self, current_page, total_pages):
        """Calculate which page numbers should be visible"""
        if total_pages <= 7:
            return list(range(1, total_pages + 1))
            
        if current_page <= 4:
            return [1, 2, 3, 4, 5, "...", total_pages]
            
        if current_page >= total_pages - 3:
            return [1, "...", total_pages-4, total_pages-3, total_pages-2, total_pages-1, total_pages]
            
        return [1, "...", current_page-1, current_page, current_page+1, "...", total_pages]
    
    def go_to_page(self, page):
        """Go to specific page number"""
        if isinstance(page, int) and page != self.current_page:
            self.current_page = page
            self.load_categories()
    
    def on_rows_per_page_change(self, value):
        """Handle change in number of rows per page"""
        self.items_per_page = int(value)
        self.current_page = 1  # Reset to first page
        self.load_categories()
    
    def update_pagination_buttons(self):
        """Update the state of pagination buttons"""
        total_pages = math.ceil(self.total_items / self.items_per_page)
        
        # Update prev button
        if self.current_page <= 1:
            self.prev_button.configure(state="disabled", fg_color="#F0F0F0")
        else:
            self.prev_button.configure(state="normal", fg_color="transparent")
            
        # Update next button
        if self.current_page >= total_pages:
            self.next_button.configure(state="disabled", fg_color="#F0F0F0")
        else:
            self.next_button.configure(state="normal", fg_color="transparent")
            
        # Update page label
        # self.page_label.configure(text=f"Page {self.current_page} of {total_pages}")
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_categories()
    
    def next_page(self):
        """Go to next page"""
        total_pages = math.ceil(self.total_items / self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_categories()
    
    def on_search(self, event=None):
        """Handle search when Enter is pressed"""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1  # Reset to first page
        self.load_categories()
    
    def load_categories(self):
        # Clear existing content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        try:
            # Get categories and apply search filter
            all_categories = self.controller.get_all_categories()
            
            # Filter categories if search query exists
            if self.search_query:
                all_categories = [
                    cat for cat in all_categories 
                    if self.search_query.lower() in cat["name"].lower() or 
                       (cat["description"] and self.search_query.lower() in cat["description"].lower())
                ]
            
            # Apply sorting based on filters
            if hasattr(self, 'name_sort') and self.name_sort.get() != "none":
                reverse = self.name_sort.get() == "desc"
                all_categories = sorted(all_categories, key=lambda x: x["name"].lower(), reverse=reverse)
            elif hasattr(self, 'desc_sort') and self.desc_sort.get() != "none":
                reverse = self.desc_sort.get() == "desc"
                all_categories = sorted(all_categories, key=lambda x: (x["description"] or "").lower(), reverse=reverse)
            
            self.total_items = len(all_categories)
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            categories = all_categories[start_idx:end_idx]

            if not categories:
                no_data_text = "No categories found"
                if self.search_query:
                    no_data_text = f'No categories found for "{self.search_query}"'
                    
                no_data_label = ctk.CTkLabel(
                    self.main_content,
                    text=no_data_text,
                    font=("", 13),
                    text_color="#6F6E77"
                )
                no_data_label.grid(row=0, column=0, columnspan=4, pady=20)
            else:
                name_width = 200
                desc_width = 300
                total_width = 120
                actions_width = 80
                
                for idx, category in enumerate(categories):
                    row_frame = ctk.CTkFrame(
                        self.main_content,
                        fg_color="transparent",
                        height=50
                    )
                    row_frame.grid(row=idx*2, column=0, columnspan=4, sticky="nsew", padx=1)
                    
                    # Configure row columns with same weights and minimum sizes
                    row_frame.grid_columnconfigure(0, weight=3, minsize=name_width)  # Name
                    row_frame.grid_columnconfigure(1, weight=5, minsize=desc_width)  # Description
                    row_frame.grid_columnconfigure(2, weight=2, minsize=total_width)  # Total Products
                    row_frame.grid_columnconfigure(3, weight=1, minsize=actions_width)  # Actions

                    # Name with fixed width
                    name_label = ctk.CTkLabel(
                        row_frame,
                        text=category["name"],
                        font=("", 13),
                        text_color="#16151C",
                        anchor="w",
                        width=name_width,
                        wraplength=name_width-30
                    )
                    name_label.grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

                    # Description with fixed width
                    description = category["description"][:50] + "..." if category["description"] and len(category["description"]) > 50 else (category["description"] or "-")
                    desc_label = ctk.CTkLabel(
                        row_frame,
                        text=description,
                        font=("", 13),
                        text_color="#16151C",
                        anchor="w",
                        width=desc_width,
                        wraplength=desc_width-20
                    )
                    desc_label.grid(row=0, column=1, padx=10, pady=15, sticky="w")

                    # Total Products with fixed width
                    total_label = ctk.CTkLabel(
                        row_frame,
                        text=str(category["total_products"]),
                        font=("", 13),
                        text_color="#16151C",
                        anchor="w",
                        width=total_width
                    )
                    total_label.grid(row=0, column=2, padx=10, pady=15, sticky="w")

                    # Actions with two buttons
                    actions_frame = ctk.CTkFrame(
                        row_frame,
                        fg_color="transparent",
                    )
                    actions_frame.grid(row=0, column=3, padx=10, pady=15, sticky="w")

                    # Edit button
                    edit_button = ctk.CTkButton(
                        actions_frame,
                        text="",
                        image=self.edit_icon,
                        fg_color="#006EC4",
                        text_color="white",
                        hover_color="#0059A1",
                        width=36,  # Adjusted width
                        height=36,  # Adjusted height
                        corner_radius=6,
                        command=lambda cat=category: self.show_edit_dialog(cat)
                    )
                    edit_button.pack(side="left", padx=(0, 5))

                    # Delete button
                    delete_button = ctk.CTkButton(
                        actions_frame,
                        text="",
                        image=self.trash_icon,
                        fg_color="#e03137",
                        text_color="white",
                        hover_color="#b32429",
                        width=36,  # Adjusted width
                        height=36,  # Adjusted height
                        corner_radius=6,
                        command=lambda cat=category: self.delete_category(cat)
                    )
                    delete_button.pack(side="left")

                    # Add separator
                    if idx < len(categories) - 1:
                        separator = ctk.CTkFrame(
                            self.main_content,
                            fg_color="#F0F0F0",
                            height=1
                        )
                        separator.grid(row=idx*2+1, column=0, columnspan=4, sticky="ew", padx=20)
            
            # Update pagination controls
            self.create_pagination_controls()
            
        except Exception as e:
            print(f"Error loading categories: {e}")
            error_label = ctk.CTkLabel(
                self.main_content,
                text=f"Error loading categories: {str(e)}",
                font=("", 13),
                text_color="#FF4842"
            )
            error_label.pack(pady=20)
    
    def show_add_dialog(self):
        """Show dialog to add a new category"""
        dialog = CategoryDialog(
            self,
            on_save=self.save_category
        )
        
    def show_edit_dialog(self, category):
        """Show dialog to edit a category"""
        dialog = CategoryDialog(
            self,
            category=category,
            on_save=self.save_category
        )
    
    def save_category(self, category_data):
        """Save or update a category"""
        try:
            if "category_id" in category_data:
                # Update existing category
                self.controller.update(
                    category_data["category_id"],
                    category_data["name"],
                    category_data["description"]
                )
            else:
                # Add new category
                self.controller.add(
                    category_data["name"],
                    category_data["description"]
                )
            # Refresh the table
            self.load_categories()
        except Exception as e:
            raise Exception(f"Failed to save category: {str(e)}")
            
    def delete_category(self, category):
        """Delete a category after confirmation"""
        # Create confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Delete Category")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        result = {"confirmed": False}
        
        def confirm():
            result["confirmed"] = True
            dialog.destroy()
            try:
                self.controller.delete(category["category_id"])
                self.load_categories()
            except Exception as e:
                self.show_error_dialog("Error", f"Failed to delete category: {str(e)}")
        
        # Add message
        message_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        message_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        heading_label = ctk.CTkLabel(
            message_frame,
            text="Delete Category",
            font=("", 16, "bold"),
            text_color="#16151C"
        )
        heading_label.pack(pady=(0, 15))
        
        message_label = ctk.CTkLabel(
            message_frame,
            text=f"Are you sure you want to delete category '{category['name']}'?\nThis action cannot be undone.",
            font=("", 13),
            text_color="#6F6E77",
            wraplength=350
        )
        message_label.pack()
        
        # Add buttons
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Delete button
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Delete",
            fg_color="#e03137",
            text_color="white",
            hover_color="#b32429",
            width=100,
            height=40,
            corner_radius=8,
            command=confirm
        )
        delete_button.pack(side="left")
    
    def show_error_dialog(self, title, message):
        """Show an error dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Add error message
        message_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=("", 13),
            text_color="#FF4842",
            wraplength=250
        )
        message_label.pack(pady=(20, 15))
        
        # Add OK button
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            command=dialog.destroy
        )
        ok_button.pack(pady=(0, 20))
    
    def show_filter_dialog(self):
        """Show filter options dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Filter Categories")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Store filter states
        self.name_sort = tk.StringVar(value="none")  # none, asc, desc
        self.desc_sort = tk.StringVar(value="none")  # none, asc, desc
        
        # Create main content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Name filter section
        name_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Name",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        name_label.pack(anchor="w", pady=(0, 10))
        
        # Name radio buttons
        name_options_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        name_options_frame.pack(fill="x")
        
        name_all = ctk.CTkRadioButton(
            name_options_frame,
            text="All",
            variable=self.name_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        name_all.pack(side="left", padx=(0, 15))
        
        name_asc = ctk.CTkRadioButton(
            name_options_frame,
            text="A-Z",
            variable=self.name_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        name_asc.pack(side="left", padx=(0, 15))
        
        name_desc = ctk.CTkRadioButton(
            name_options_frame,
            text="Z-A",
            variable=self.name_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        name_desc.pack(side="left")
        
        # Description filter section
        desc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        desc_frame.pack(fill="x", pady=(0, 20))
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Description",
            font=("", 14, "bold"),
            text_color="#16151C"
        )
        desc_label.pack(anchor="w", pady=(0, 10))
        
        # Description radio buttons
        desc_options_frame = ctk.CTkFrame(desc_frame, fg_color="transparent")
        desc_options_frame.pack(fill="x")
        
        desc_all = ctk.CTkRadioButton(
            desc_options_frame,
            text="All",
            variable=self.desc_sort,
            value="none",
            font=("", 13),
            text_color="#16151C"
        )
        desc_all.pack(side="left", padx=(0, 15))
        
        desc_asc = ctk.CTkRadioButton(
            desc_options_frame,
            text="A-Z",
            variable=self.desc_sort,
            value="asc",
            font=("", 13),
            text_color="#16151C"
        )
        desc_asc.pack(side="left", padx=(0, 15))
        
        desc_desc = ctk.CTkRadioButton(
            desc_options_frame,
            text="Z-A",
            variable=self.desc_sort,
            value="desc",
            font=("", 13),
            text_color="#16151C"
        )
        desc_desc.pack(side="left")
        
        # Add buttons
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        buttons_frame.pack_propagate(False)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#F8F9FA",
            text_color="#16151C",
            hover_color="#E8E9EA",
            width=100,
            height=40,
            corner_radius=8,
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Apply button
        apply_button = ctk.CTkButton(
            buttons_frame,
            text="Apply",
            fg_color="#006EC4",
            text_color="white",
            hover_color="#0059A1",
            width=100,
            height=40,
            corner_radius=8,
            command=lambda: self.apply_filters(dialog)
        )
        apply_button.pack(side="left")
    
    def apply_filters(self, dialog):
        """Apply the selected filters and refresh the table"""
        dialog.destroy()
        self.current_page = 1  # Reset to first page
        self.load_categories()
