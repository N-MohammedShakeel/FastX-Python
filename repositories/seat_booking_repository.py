from utils.db import get_connection
from utils.logger import log_error

class SeatBookingRepository:
    def create_seat_booking(self, booking_id, bus_id, seat_number, conn_inherited=None):
        conn = conn_inherited if conn_inherited else get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO seat_bookings (booking_id, bus_id, seat_number) VALUES (%s, %s, %s)",
                (booking_id, bus_id, seat_number)
            )
            if not conn_inherited: conn.commit()
            return True
        except Exception as exception:
            log_error(f"Seat booking creation failed. Booking ID: {booking_id}, Seat: {seat_number}. Error: {exception}")
            raise
        finally:
            if not conn_inherited: conn.close()

    def get_booked_seats(self, bus_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT seat_number FROM seat_bookings WHERE bus_id = %s", 
                (bus_id,)
            )
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()

    def delete_booking_seats(self, booking_id, conn_inherited=None):
        conn = conn_inherited if conn_inherited else get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM seat_bookings WHERE booking_id = %s", 
                (booking_id,)
            )
            if not conn_inherited: conn.commit()
            return True
        except Exception as exception:
            log_error(f"Seat deletion failed. Booking ID: {booking_id}. Error: {exception}")
            raise
        finally:
            if not conn_inherited: conn.close()

    def get_seat_layout(self, bus_id, total_seats):
        booked = self.get_booked_seats(bus_id)
        layout = []
        for seat in range(1, total_seats + 1):
            if seat in booked:
                layout.append("--")
            else:
                layout.append(f"{seat}")

        return layout