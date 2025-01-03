import os
import sys
import bcrypt

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.models.user_model import UserModel

def create_admin_user():
    """Create an admin user"""
    try:
        # Admin credentials
        username = "admin"
        password = "admin123"  # This is just an initial password that should be changed
        email = "admin@warehouse.com"
        
        # Hash the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user model
        user_model = UserModel()
        
        # Check if admin already exists
        if user_model.get_by_username(username):
            print("Admin user already exists!")
            return
            
        # Create admin user
        user_model.create_user(
            username=username,
            password=hashed.decode('utf-8'),
            email=email,
            is_admin=True
        )
        
        print("Admin user created successfully!")
        print("Username:", username)
        print("Password:", password)
        print("\nPlease change the password after first login!")
        
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_admin_user()
