import os
import sys
import tkinter as tk

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.views.login_view import LoginView
from app.config.init_db import init_database

def main():
    # Initialize database and create admin account if needed
    init_database()
    
    root = tk.Tk()
    root.title("Quản lý kho hàng")
    
    # Set default font for the application
    default_font = ('Helvetica', 12)
    root.option_add("*Font", default_font)
    
    # Set initial window size
    window_width = 1024
    window_height = 768
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
