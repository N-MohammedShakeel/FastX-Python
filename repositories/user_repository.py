from utils.db import get_connection
from models.user import User
from utils.logger import log_error

class UserRepository:
    def find_by_id(self, user_id):
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE id = %s", 
                (user_id,)
            )
            result = cursor.fetchone()
            if result:
                return User(result['id'], result['name'], result['email'], result['password'], result['role'], result['wallet'])
            return None
        finally:
            conn.close()

    def find_by_email(self, email):
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE email = %s", 
                (email,)
            )
            result = cursor.fetchone()
            if result:
                return User(result['id'], result['name'], result['email'], result['password'], result['role'], result['wallet'])
            return None
        finally:
            conn.close()

    def save(self, user):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password, role, wallet) VALUES (%s, %s, %s, %s, %s)",
                (user.name, user.email, user.password, user.role, user.wallet)
            )
            conn.commit()
            return True
        except Exception as exception:
            log_error(f"Save User failed: {exception}")
            raise
        finally:
            conn.close()

    def update_wallet(self, user_id, amount, conn_inherited=None):
        conn = conn_inherited if conn_inherited else get_connection()

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET wallet=%s WHERE id=%s",
                (amount, user_id)
            )
            if not conn_inherited:
                conn.commit()
            return True
        except Exception as exception:
            log_error(f"Wallet update failed. User ID: {user_id}. Error: {exception}")
            raise
        finally:
            if not conn_inherited:
                conn.close()

    def get_passenger_count(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'PASSENGER'")
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def get_operator_count(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'OPERATOR'")
            return cursor.fetchone()[0]
        finally:
            conn.close()
            
    def view_users_by_role(self, role):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, name, email, wallet FROM users WHERE role = %s", 
                (role,)
            )
            return cursor.fetchall()
        finally:
            conn.close()