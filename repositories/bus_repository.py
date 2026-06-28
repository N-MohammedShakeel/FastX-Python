from utils.db import get_connection
from models.bus import Bus
from utils.logger import log_error

class BusRepository:
    def save(self, bus):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO buses (bus_name, origin, destination, journey_date, departure_time, total_seats, available_seats, operator_id, ticket_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (bus.bus_name, bus.origin, bus.destination, bus.journey_date, bus.departure_time, bus.total_seats, bus.available_seats, bus.operator_id, bus.ticket_price)
            )
            conn.commit()
            return True
        except Exception as exception:
            log_error(f"Save Bus failed: {exception}")
            raise

        finally:
            conn.close()

    def find_by_id(self, bus_id):
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM buses WHERE id = %s", 
                (bus_id,)
            )
            result = cursor.fetchone()
            if result:
                return Bus(result['id'], result['bus_name'], result['origin'], result['destination'], result['journey_date'], result['departure_time'], result['total_seats'], result['available_seats'], result['operator_id'], result['ticket_price'])
            return None
        finally:
            conn.close()

    def find_all(self):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM buses")
            return cursor.fetchall()
        finally:
            conn.close()

    def search(self, origin, destination, date_str):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM buses WHERE origin = %s AND destination = %s AND journey_date = %s", 
                (origin, destination, date_str)
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def update(self, bus):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE buses SET bus_name=%s, origin=%s, destination=%s, journey_date=%s, departure_time=%s, total_seats=%s, available_seats=%s, ticket_price=%s WHERE id=%s",
                (bus.bus_name, bus.origin, bus.destination, bus.journey_date, bus.departure_time, bus.total_seats, bus.available_seats, bus.ticket_price, bus.id)
            )
            conn.commit()
            return True
        except Exception as exception:
            log_error(f"Bus Update failed. Bus ID: {bus.id}, Error: {exception}")
            raise
        finally:
            conn.close()

    def delete(self, bus_id, operator_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM buses WHERE id = %s AND operator_id = %s", 
                (bus_id, operator_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as exception:
            log_error(f"Bus Deletion failed. Bus ID: {bus_id}, Error: {exception}")
            raise
        finally:
            conn.close()

    def find_by_operator(self, operator_id):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM buses WHERE operator_id = %s", 
                (operator_id,)
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def count_operator_buses(self, operator_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM buses WHERE operator_id = %s", 
                (operator_id,)
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()