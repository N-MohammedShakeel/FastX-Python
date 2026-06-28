from utils.db import get_connection
from models.booking import Booking
from utils.logger import log_error

class BookingRepository:
    def save(self, booking, conn_inherited=None):
        conn = conn_inherited if conn_inherited else get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bookings (passenger_id, bus_id, seat_count, booking_date, status, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
                (booking.passenger_id, booking.bus_id, booking.seat_count, booking.booking_date, booking.status, booking.total_price)
            )
            if not conn_inherited: conn.commit()
            return cursor.lastrowid
        
        except Exception as exception:
            log_error(f"BookingRepository.save() failed: {exception}")
            raise
        
        finally:
            if not conn_inherited: conn.close()

    def find_by_id(self, booking_id):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM bookings WHERE id = %s", 
                (booking_id,)
            )
            result = cursor.fetchone()
            if result:
                return Booking(result['id'], result['passenger_id'], result['bus_id'], result['seat_count'], result['booking_date'], result['status'], result['total_price'])
            return None
        finally:
            conn.close()

    def find_by_passenger(self, passenger_id):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT b.id as booking_id, bus.bus_name, bus.origin, bus.destination, bus.journey_date, b.seat_count, b.booking_date, b.status, b.total_price FROM bookings b JOIN buses bus ON b.bus_id = bus.id WHERE b.passenger_id = %s", 
                (passenger_id,)
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def find_by_operator(self, operator_id):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT b.id as booking_id, u.name as passenger_name, bus.bus_name, b.seat_count, b.booking_date, b.status, b.total_price FROM bookings b JOIN buses bus ON b.bus_id = bus.id JOIN users u ON b.passenger_id = u.id WHERE bus.operator_id = %s",
                (operator_id,)
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def find_all_bookings_dashboard(self):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT b.id as booking_id, u.name as passenger_name, bus.bus_name, bus.origin, bus.destination, b.seat_count, b.status, b.total_price FROM bookings b JOIN buses bus ON b.bus_id = bus.id JOIN users u ON b.passenger_id = u.id"
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def update_status(self, booking_id, status, conn_inherited=None):
        conn = conn_inherited if conn_inherited else get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE bookings SET status = %s WHERE id = %s", 
                (status, booking_id)
            )
            if not conn_inherited: conn.commit()
            return True
        except Exception as exception:
            log_error(f"Booking status update failed. Booking ID: {booking_id}. Error: {exception}")
            raise

        finally:
            if not conn_inherited: conn.close()

    def count_passenger_bookings(self, passenger_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM bookings WHERE passenger_id = %s AND status = 'BOOKED'", 
                (passenger_id,)
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def count_passenger_cancellations(self, passenger_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM bookings WHERE passenger_id = %s AND status = 'CANCELLED'", 
                (passenger_id,)
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def count_operator_bookings(self, operator_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM bookings b JOIN buses bus ON b.bus_id = bus.id WHERE bus.operator_id = %s AND b.status='BOOKED'", 
                (operator_id,)
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def count_operator_cancellations(self, operator_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM bookings b JOIN buses bus ON b.bus_id = bus.id WHERE bus.operator_id = %s AND b.status='CANCELLED'", 
                (operator_id,)
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def count_all_bookings(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'BOOKED'")
            return cursor.fetchone()[0]
        finally:
            conn.close()