from app.models.base_model import BaseModel

class UserModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._ensure_approval_column()

    def _ensure_approval_column(self):
        """Ensure the approval_status column exists"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'is_approved'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN is_approved BOOLEAN DEFAULT FALSE
                """)
                self.conn.commit()
        except Exception as e:
            print(f"Error ensuring approval column: {str(e)}")

    def get_all(self):
        """Get all users with their roles and approval status"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            ORDER BY u.username
        """)
        return cursor.fetchall()

    def get_pending_users(self):
        """Get users pending approval"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            WHERE u.is_approved = FALSE
            ORDER BY u.username
        """)
        return cursor.fetchall()

    def approve_user(self, user_id):
        """Approve a user and set role_id to 3"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE users 
                SET is_approved = TRUE, role_id = 3
                WHERE user_id = %s
            """, (user_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error approving user: {str(e)}")
            return False

    def reject_user(self, user_id):
        """Reject and delete a user"""
        return self.delete_user(user_id)

    def create_user(self, username, password, email, is_admin=False):
        """Create a new user"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            # Get role ID
            role_name = 'administrator' if is_admin else 'registered_user'
            cursor.execute(
                "SELECT role_id FROM user_roles WHERE role_name = %s",
                (role_name,)
            )
            role = cursor.fetchone()
            if not role:
                raise Exception(f"Role '{role_name}' not found")

            # Insert user with approval status
            cursor.execute("""
                INSERT INTO users (username, password, email, role_id, is_approved)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, email, role['role_id'], is_admin))  # Admins are auto-approved
            
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    def verify_login(self, username, password):
        """Verify login credentials and approval status"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            WHERE u.username = %s AND u.password = %s
        """, (username, password))
        user = cursor.fetchone()
        
        if not user:
            return False, "Invalid username or password"
        
        if not user['is_approved'] and user['role_name'] != 'administrator':
            return False, "Your account is pending approval"
            
        return True, user

    def add(self, data):
        """Add a new user - implemented through create_user method"""
        return self.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            is_admin=data.get('is_admin', False)
        )

    def update(self, id, data):
        """Update a user - implemented through update_user method"""
        return self.update_user(id, data)

    def delete(self, id):
        """Delete a user - implemented through delete_user method"""
        return self.delete_user(id)

    def get_by_username(self, username):
        """Get user by username"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            WHERE u.username = %s
        """, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_by_email(self, email):
        """Get user by email"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            WHERE u.email = %s
        """, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_by_id(self, user_id):
        """Get user by ID"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, r.role_name 
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
            WHERE u.user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_user(self, user_id, data):
        """Update user information"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            # Build update query dynamically based on provided data
            update_fields = []
            values = []
            for key, value in data.items():
                if key in ['username', 'email', 'password']:
                    update_fields.append(f"{key} = %s")
                    values.append(value)

            if not update_fields:
                return False

            # Add user_id to values
            values.append(user_id)

            # Execute update query
            query = f"""
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE user_id = %s
            """
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def update_password(self, user_id, new_password):
        """Update user password"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                UPDATE users 
                SET password = %s
                WHERE user_id = %s
            """, (new_password, user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete_user(self, user_id):
        """Delete a user"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                DELETE FROM users 
                WHERE user_id = %s
            """, (user_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_roles(self):
        """Get all user roles except administrator"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM user_roles
                WHERE role_name IN ('user', 'manager')
                ORDER BY role_name
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting roles: {str(e)}")
            return []

    def get_approved_users(self):
        """Get approved users"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.*, r.role_name 
                FROM users u
                JOIN user_roles r ON u.role_id = r.role_id
                WHERE u.is_approved = TRUE
                ORDER BY u.username
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting approved users: {str(e)}")
            return []

    def get_users_with_pagination(self, offset=0, limit=10, search_query=""):
        """Get users with pagination and optional search query"""
        cursor = self.conn.cursor(dictionary=True)
        try:
            # Build the base query
            query = """
                SELECT u.*, r.role_name 
                FROM users u
                JOIN user_roles r ON u.role_id = r.role_id
            """
            # Add search condition if search_query is provided
            if search_query:
                query += " WHERE u.username LIKE %s OR u.email LIKE %s"
                search_term = f"%{search_query}%"
                cursor.execute(query + " ORDER BY u.username LIMIT %s OFFSET %s", (search_term, search_term, limit, offset))
            else:
                cursor.execute(query + " ORDER BY u.username LIMIT %s OFFSET %s", (limit, offset))
            
            users = cursor.fetchall()

            # Get total count for pagination
            cursor.execute("SELECT COUNT(*) FROM users")
            total_count = cursor.fetchone()['COUNT(*)']

            return users, total_count
        except Exception as e:
            print(f"Error fetching users with pagination: {str(e)}")
            return [], 0
        finally:
            cursor.close()

    def set_user_role(self, user_id, new_role):
        """Update the role of a user identified by user_id."""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # Fetch the role_id for the new_role
            cursor.execute("SELECT role_id FROM user_roles WHERE role_name = %s", (new_role,))
            role = cursor.fetchone()
            if not role:
                print(f"Role '{new_role}' not found.")
                return False

            # Update the user's role_id
            cursor.execute("UPDATE users SET role_id = %s WHERE user_id = %s", (role['role_id'], user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Error in UserModel.set_user_role: {e}")
            return False
        finally:
            cursor.close()
