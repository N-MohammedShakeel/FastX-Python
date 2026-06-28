from services.operator_service import OperatorService
from utils.decorators import check_authentication, role_allowed

ROLE_OPERATOR = "OPERATOR"

class OperatorController:
    def __init__(self):
        self.operator_service = OperatorService()

    @check_authentication
    @role_allowed(ROLE_OPERATOR)
    def add_bus(self, name, origin, destination, date, time, total_seats, operator_id, ticket_price):
        if self.operator_service.add_bus(name, origin.lower(), destination.lower(), date, time, total_seats, operator_id, ticket_price):
            print("SUCCESS: Bus Registered Successfully.")
        else:
            print("ERROR: Bus Registration Failed.")

    @check_authentication
    @role_allowed(ROLE_OPERATOR)
    def update_bus(self, bus_id, operator_id, name, origin, destination, date, time, ticket_price):
        try:
            if self.operator_service.update_bus(bus_id, operator_id, name, origin, destination, date, time, ticket_price):
                print("SUCCESS: Bus Updated Successfully.")
        except Exception as exception:
            print("ERROR: Bus Updation Failed.", exception)

    @check_authentication
    @role_allowed(ROLE_OPERATOR)
    def delete_bus(self, bus_id, operator_id):
        if self.operator_service.delete_bus(bus_id, operator_id):
            print("SUCCESS: Bus Deleted Successfully")
        else:
            print("ERROR: Bus Deletion Failed.")

    @check_authentication
    @role_allowed(ROLE_OPERATOR)
    def view_fleet(self, operator_id):
        buses = self.operator_service.view_my_buses(operator_id)
        print("\n=== OPERATOR FLEET ===")
        if not buses:
            print("No buses registered.")
            return
        for bus in buses:
            print(f"Bus ID: {bus['id']} \nBus Name: {bus['bus_name']} \nRoute: {bus['origin']}->{bus['destination']} \nTicket Price: {bus['ticket_price']} \nAvailable Seats: {bus['available_seats']}/{bus['total_seats']}\n")
            
    @check_authentication
    @role_allowed(ROLE_OPERATOR)
    def view_bookings(self, operator_id):
        bookings = self.operator_service.view_bus_bookings(operator_id)
        print("\n=== OPERATOR BOOKINGS ===")
        if not bookings:
            print("No bookings available.")
            return
        for booking in bookings:
            print(f"Booking ID: {booking['booking_id']} \nPassenger: {booking['passenger_name']} \nEngine Label: {booking['bus_name']} \nSeats Filled: {booking['seat_count']} \nStatus: {booking['status']}\n")

    @check_authentication
    @role_allowed(ROLE_OPERATOR)
    def show_dashboard(self, operator_id, operator_name):
        stats = self.operator_service.get_dashboard_stats(operator_id)
        print("\n====== OPERATOR STATS ======")
        print(f"Welcome, {operator_name}")
        print(f"Wallet Balance: {stats['wallet']}")
        print(f"Total Buses: {stats['buses']}")
        print(f"Confirmed Bookings: {stats['bookings']}")
        print(f"Cancelled Bookings: {stats['cancellations']}")