from utils.db import get_connection
from utils.logger import log_info, log_error

class OperatorService:

    def add_bus(self, name, src, dest, date_str, time_str, total_seats, operator_id):
        """Constructs tracking metadata parameters for deployment arrays."""
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO buses (bus_name, source, destination, journey_date, departure_time, total_seats, available_seats, operator_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, src, dest, date_str, time_str, total_seats, total_seats, operator_id))
            conn.commit()
            log_info(f"Operator Added Bus: {name} running from {src} to {dest}")
            return True
        except Exception as exception:
            log_error(f"Add Bus Query Aborted: {exception}")
            return False
        finally:
            conn.close()

    def view_my_buses(self, operator_id):
        """Collects operational mapping entities configured by this user."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM buses WHERE operator_id = %s", (operator_id,))
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"Operator View Fleet Failed: {exception}")
            return []
        finally:
            conn.close()

    def delete_bus(self, bus_id, operator_id):
        """Removes records safely, leveraging foreign key cascade patterns."""
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM buses WHERE id = %s AND operator_id = %s"
            cursor.execute(query, (bus_id, operator_id))
            conn.commit()
            log_info(f"Bus Deleted: ID {bus_id} processed by Operator {operator_id}")
            return True
        except Exception as exception:
            log_error(f"Delete Fleet Target Aborted: {exception}")
            return False
        finally:
            conn.close()

    def view_bus_bookings(self, operator_id):
        """Compiles passenger data variables attached to this user's asset IDs."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT b.id as booking_id, u.name as passenger_name, bus.bus_name, 
                       b.seat_count, b.booking_date 
                FROM bookings b
                JOIN buses bus ON b.bus_id = bus.id
                JOIN users u ON b.passenger_id = u.id
                WHERE bus.operator_id = %s
            """
            cursor.execute(query, (operator_id,))
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"Operator View Bookings Failed: {exception}")
            return []
        finally:
            conn.close()