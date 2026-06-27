from utils.db import get_connection
from utils.logger import log_error

class AdminService:
    def view_users(self):
        """Compiles passenger identity values stored inside user directory vectors."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, email FROM users WHERE role = 'PASSENGER'")
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"Admin View Users Query Failed: {exception}")
            return []
        finally:
            conn.close()

    def view_operators(self):
        """Compiles company tracking values stored inside directory listings."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, email FROM users WHERE role = 'OPERATOR'")
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"Admin View Operators Query Failed: {exception}")
            return []
        finally:
            conn.close()

    def view_all_bookings(self):
        """Extracts complete system reservation logs across global variables."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT b.id as booking_id, u.name as passenger_name, bus.bus_name, 
                       bus.source, bus.destination, b.seat_count, b.booking_date 
                FROM bookings b
                JOIN buses bus ON b.bus_id = bus.id
                JOIN users u ON b.passenger_id = u.id
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"Admin View All Bookings Failed: {exception}")
            return []
        finally:
            conn.close()