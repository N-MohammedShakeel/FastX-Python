from datetime import datetime
from repositories.user_repository import UserRepository
from repositories.bus_repository import BusRepository
from repositories.booking_repository import BookingRepository
from repositories.seat_booking_repository import SeatBookingRepository
from models.booking import Booking
from utils.db import get_connection
from utils.logger import log_info, log_warning, log_error
from exceptions.bus_not_found_exception import BusNotFoundException
from exceptions.insufficient_seats_exception import InsufficientSeatsException
from exceptions.invalid_seat_selection_exception import InvalidSeatSelectionException
from exceptions.insufficient_balance_exception import InsufficientBalanceException
from exceptions.user_not_found_exception import UserNotFoundException

class PassengerService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.bus_repo = BusRepository()
        self.booking_repo = BookingRepository()
        self.seat_repo = SeatBookingRepository()

    def view_all_buses(self):
        return self.bus_repo.find_all()

    def search_buses(self, origin, destination, date_str):
        return self.bus_repo.search(origin, destination, date_str)

    def add_money(self, user_id, amount):
        user = self.user_repo.find_by_id(user_id)
        if not user: 
            raise UserNotFoundException()
        
        user.deposit_money(amount)
        return self.user_repo.update_wallet(user_id, user.wallet)

    def get_wallet(self, user_id):
        user = self.user_repo.find_by_id(user_id)
        if user:
            return user.wallet
        else:
            raise UserNotFoundException()

    def get_dashboard_stats(self, user_id):
        return {
            "wallet": self.get_wallet(user_id),
            "bookings": self.booking_repo.count_passenger_bookings(user_id),
            "cancellations": self.booking_repo.count_passenger_cancellations(user_id)
        }

    def view_my_bookings(self, user_id):
        return self.booking_repo.find_by_passenger(user_id)

    def book_ticket(self, passenger_id, bus_id, seat_list):

        bus = self.bus_repo.find_by_id(bus_id)
        if not bus:
            log_warning(f"Booking failed. Bus {bus_id} not found.") 
            raise BusNotFoundException()
        
        seat_count = len(seat_list)

        if len(set(seat_list)) != len(seat_list):
            log_warning(f"Passenger {passenger_id} selected duplicate seats {seat_list}")
            raise InvalidSeatSelectionException("Duplicate seat numbers are not allowed.")

        if bus.available_seats < seat_count: 
            log_warning(f"Passenger {passenger_id} tried booking {seat_count} seats but only {bus.available_seats} available.")
            raise InsufficientSeatsException()

        booked = self.seat_repo.get_booked_seats(bus_id)
        for seat in seat_list:
            if seat <= 0 or seat > bus.total_seats or seat in booked:
                log_warning(f"Passenger {passenger_id} selected invalid seat {seat} for Bus {bus_id}")
                raise InvalidSeatSelectionException(f"Seat {seat} invalid or already booked.")

        passenger = self.user_repo.find_by_id(passenger_id)
        operator = self.user_repo.find_by_id(bus.operator_id)
        
        total_price = bus.ticket_price * seat_count
        if passenger.wallet < total_price: 
            log_warning(f"Passenger {passenger_id} has insufficient balance.")
            raise InsufficientBalanceException()

        conn = get_connection()
        try:
            passenger.deduct_money(total_price)
            operator.deposit_money(total_price)
            bus.allocate_seats(seat_count)
            
            self.user_repo.update_wallet(passenger.id, passenger.wallet, conn_inherited=conn)
            self.user_repo.update_wallet(operator.id, operator.wallet, conn_inherited=conn)
            self.bus_repo.update(bus)
            
            new_booking = Booking(None, passenger_id, bus_id, seat_count, datetime.now().strftime("%Y-%m-%d"), 'BOOKED', total_price)
            booking_id = self.booking_repo.save(new_booking, conn_inherited=conn)
            
            for seat in seat_list:
                self.seat_repo.create_seat_booking(booking_id, bus_id, seat, conn_inherited=conn)
            
            log_info(f"Booking Successful for Booking ID: {booking_id}, Passenger: {passenger_id}, Bus: {bus_id}, Seats: {seat_list}, Amount: {total_price}")
            conn.commit()
            return True
        except Exception as exception:
            conn.rollback()
            log_error(f"Booking Failed for Passenger: {passenger_id}, Bus: {bus_id}, Error: {exception}")
            raise exception
        finally:
            conn.close()

    def cancel_booking(self, passenger_id, booking_id):

        booking = self.booking_repo.find_by_id(booking_id)

        if not booking or booking.passenger_id != passenger_id or booking.status == 'CANCELLED':
            print("ERROR: Booking not found or already cancelled.")
            log_warning(f"Cancellation failed. Booking {booking_id} not found.")
            return False

        bus = self.bus_repo.find_by_id(booking.bus_id)
        passenger = self.user_repo.find_by_id(passenger_id)
        operator = self.user_repo.find_by_id(bus.operator_id)

        if not passenger or not operator:
            raise UserNotFoundException()

        if not bus:
            raise BusNotFoundException()
        
        refund = booking.total_price

        conn = get_connection()
        try:
            operator.deduct_money(refund)
            passenger.deposit_money(refund)
            bus.release_seats(booking.seat_count)
            
            self.booking_repo.update_status(booking_id, 'CANCELLED', conn_inherited=conn)
            self.seat_repo.delete_booking_seats(booking_id, conn_inherited=conn)            
            self.bus_repo.update(bus)
            self.user_repo.update_wallet(passenger.id, passenger.wallet, conn_inherited=conn)
            self.user_repo.update_wallet(operator.id, operator.wallet, conn_inherited=conn)
            
            log_info(f"Booking {booking_id} cancelled successfully. Refunded amount: {refund}")
            conn.commit()
            return True
        except Exception as exception:
            log_error(f"Cancellation failed. Booking {booking_id}. Error: {exception}")
            print(f"ERROR: Cancellation Failed. {exception}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_seat_layout(self, bus_id):

        bus = self.bus_repo.find_by_id(bus_id)
        if not bus:
            log_warning(f"Seat layout requested for invalid Bus ID {bus_id}")
            raise BusNotFoundException()
        return self.seat_repo.get_seat_layout(
            bus.id,
            bus.total_seats
        )