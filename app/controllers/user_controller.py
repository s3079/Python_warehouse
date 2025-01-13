from app.models.user_model import UserModel
import bcrypt

class UserController:
    def __init__(self):
        self.model = UserModel()

    def get_all(self):
        """Get all users"""
        try:
            return self.model.get_all()
        except Exception as e:
            print(f"Error getting users: {str(e)}")
            return []

    def get_pending_users(self):
        """Get users pending approval"""
        try:
            return self.model.get_pending_users()
        except Exception as e:
            print(f"Error getting pending users: {str(e)}")
            return []

    def approve_user(self, user_id):
        """Approve a user"""
        try:
            return self.model.approve_user(user_id)
        except Exception as e:
            print(f"Error approving user: {str(e)}")
            return False

    def reject_user(self, user_id):
        """Reject a user"""
        try:
            return self.model.reject_user(user_id)
        except Exception as e:
            print(f"Error rejecting user: {str(e)}")
            return False

    def login(self, username, password):
        """
        Authenticate user login
        Returns: (success, result)
            - If success is True, result is user data
            - If success is False, result is error message
        """
        try:
            # Get user by username
            user = self.model.get_by_username(username)
            if not user:
                return False, "Invalid username or password"

            # Check password
            if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return False, "Invalid username or password"

            # Remove password from user data before returning
            user_data = {k: v for k, v in user.items() if k != 'password'}
            print("User logged in:", user_data)
            return True, user_data

        except Exception as e:
            return False, f"Login error: {str(e)}"

    def register(self, username, password, email):
        """
        Register a new user
        Returns: (success, message)
        """
        try:
            # Check if username already exists
            if self.model.get_by_username(username):
                return False, "Username already exists"

            # Check if email already exists
            if self.model.get_by_email(email):
                return False, "Email already exists"

            # Hash password
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user (default to non-admin)
            self.model.create_user(username, hashed.decode('utf-8'), email, is_admin=False)
            
            return True, "Registration successful! Please wait for admin approval."

        except Exception as e:
            return False, f"Registration error: {str(e)}"

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.model.get_by_id(user_id)
            if user:
                # Remove password from user data
                user_data = {k: v for k, v in user.items() if k != 'password'}
                return True, user_data
            return False, "User not found"
        except Exception as e:
            return False, f"Error retrieving user: {str(e)}"

    def update_user(self, user_id, data):
        """Update user information"""
        try:
            if 'password' in data:
                # Hash new password if provided
                data['password'] = bcrypt.hashpw(
                    data['password'].encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
            
            success = self.model.update_user(user_id, data)
            if success:
                return True, "User updated successfully"
            return False, "Failed to update user"
        except Exception as e:
            return False, f"Error updating user: {str(e)}"

    def delete_user(self, user_id):
        """Delete a user"""
        try:
            success = self.model.delete_user(user_id)
            if success:
                return True, "User deleted successfully"
            return False, "Failed to delete user"
        except Exception as e:
            return False, f"Error deleting user: {str(e)}"

    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            # Get user
            user = self.model.get_by_id(user_id)
            if not user:
                return False, "User not found"

            # Verify old password
            if not bcrypt.checkpw(old_password.encode('utf-8'), 
                                user['password'].encode('utf-8')):
                return False, "Current password is incorrect"

            # Hash and update new password
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            success = self.model.update_password(user_id, hashed.decode('utf-8'))
            
            if success:
                return True, "Password changed successfully"
            return False, "Failed to change password"
            
        except Exception as e:
            return False, f"Error changing password: {str(e)}"

    def get_roles(self):
        """Get all user roles"""
        try:
            return self.model.get_roles()
        except Exception as e:
            print(f"Error getting roles: {str(e)}")
            return []

    def get_approved_users(self):
        """Get approved users"""
        try:
            return self.model.get_approved_users()
        except Exception as e:
            print(f"Error getting approved users: {str(e)}")
            return []

    def get_users_paginated(self, offset=0, limit=10, search_query=""):
        """Fetch users with pagination and optional search query"""
        try:
            users, total_count = self.model.get_users_with_pagination(
                offset=offset,
                limit=limit,
                search_query=search_query
            )
            return users, total_count
        except Exception as e:
            print(f"Error fetching paginated users: {str(e)}")
            return [], 0

    def set_user_role(self, user_id, new_role):
        """Set the role of a user identified by user_id to new_role."""
        try:
            # Use UserModel to update the user's role
            success = self.model.set_user_role(user_id, new_role)
            if success:
                return True
            return False
        except Exception as e:
            print(f"Error updating user role: {e}")
            return False
