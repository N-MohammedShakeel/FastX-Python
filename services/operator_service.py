from repositories.bus_repository import BusRepository
from repositories.booking_repository import BookingRepository
from repositories.user_repository import UserRepository
from exceptions.bus_not_found_exception import BusNotFoundException
from models.bus import Bus
from utils.logger import log_info, log_warning

class OperatorService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.bus_repo = BusRepository()
        self.booking_repo = BookingRepository()

    def add_bus(self, name, origin, destination, date, time, total_seats, operator_id, ticket_price):
        
        new_bus = Bus(None, name, origin, destination, date, time, total_seats, total_seats, operator_id, ticket_price)
        status = self.bus_repo.save(new_bus)

        if status:
            log_info(f"Operator {operator_id} registered Bus '{name}'")
        else:
            log_warning(f"Bus registration failed for Operator {operator_id}")

        return status

    def update_bus(self, bus_id, operator_id, name, origin, destination, date, time, ticket_price):
        
        bus = self.bus_repo.find_by_id(bus_id)
        if not bus or bus.operator_id != operator_id: 
            log_warning(f"Operator {operator_id} attempted to update invalid Bus {bus_id}")
            raise BusNotFoundException()
        
        bus.bus_name = name
        bus.origin = origin
        bus.destination = destination
        bus.journey_date = date
        bus.departure_time = time
        bus.ticket_price = ticket_price

        log_info(f"Bus {bus_id} updated by Operator {operator_id}")
        return self.bus_repo.update(bus)

    def delete_bus(self, bus_id, operator_id):
        status = self.bus_repo.delete(bus_id, operator_id)

        if status:
            log_info(f"Bus {bus_id} deleted by Operator {operator_id}")
        else:
            log_warning(f"Delete failed for Bus {bus_id}")

        return status

    def view_my_buses(self, operator_id):
        return self.bus_repo.find_by_operator(operator_id)

    def view_bus_bookings(self, operator_id):
        return self.booking_repo.find_by_operator(operator_id)
    
    def get_wallet(self, user_id):
        user = self.user_repo.find_by_id(user_id)
        if user:
            return user.wallet
        else:
            return 0
        
    def get_dashboard_stats(self, operator_id):
        return {
            "wallet": self.get_wallet(operator_id),
            "buses": self.bus_repo.count_operator_buses(operator_id),
            "bookings": self.booking_repo.count_operator_bookings(operator_id),
            "cancellations": self.booking_repo.count_operator_cancellations(operator_id)
        }