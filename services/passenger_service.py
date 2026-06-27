from datetime import datetime
from utils.db import get_connection
from utils.logger import log_info, log_error

class PassengerService:

    def view_all_buses(self):
        """Fetches all schedules registered in the system."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM buses")
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"View Buses Query Failed: {exception}")
            return []
        finally:
            conn.close()

    def search_buses(self, src, dest, date_str):
        """Filters scheduling lists tracking matching geographical vectors."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM buses WHERE source = %s AND destination = %s AND journey_date = %s"
            cursor.execute(query, (src, dest, date_str))
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"Search Route Query Failed: {exception}")
            return []
        finally:
            conn.close()

    def book_ticket(self, passenger_id, bus_id, seat_count):
        """Deducts database integers and registers tracking records safely."""
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT available_seats FROM buses WHERE id = %s", (bus_id,))
            bus = cursor.fetchone()
            
            if not bus or bus["available_seats"] < seat_count:
                log_error("Booking Failed: Insufficient seat inventory capacity available.")
                return False
                
            new_seats = bus["available_seats"] - seat_count
            cursor.execute("UPDATE buses SET available_seats = %s WHERE id = %s", (new_seats, bus_id))
            
            today = datetime.now().strftime("%Y-%m-%d")
            booking_query = "INSERT INTO bookings (passenger_id, bus_id, seat_count, booking_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(booking_query, (passenger_id, bus_id, seat_count, today))
            
            conn.commit()
            log_info(f"Ticket Booked: User ID {passenger_id} locked {seat_count} seats on Bus ID {bus_id}")
            return True
        except Exception as exception:
            conn.rollback()
            log_error(f"Booking Process Crashed: {exception}")
            return False
        finally:
            conn.close()

    def get_my_bookings(self, passenger_id):
        """Gathers relational join data lists specifying user asset matching."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT b.id as booking_id, bus.bus_name, bus.source, bus.destination, 
                       bus.journey_date, b.seat_count, b.booking_date 
                FROM bookings b
                JOIN buses bus ON b.bus_id = bus.id
                WHERE b.passenger_id = %s
            """
            cursor.execute(query, (passenger_id,))
            return cursor.fetchall()
        except Exception as exception:
            log_error(f"My Bookings Query Failed: {exception}")
            return []
        finally:
            conn.close()