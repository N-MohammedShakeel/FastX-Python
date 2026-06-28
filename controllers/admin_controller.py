from services.admin_service import AdminService
from utils.decorators import check_authentication, role_allowed

ROLE_ADMIN = "ADMIN"

class AdminController:
    def __init__(self):
        self.admin_service = AdminService()
    @check_authentication
    @role_allowed(ROLE_ADMIN)
    def view_passengers(self):
        users = self.admin_service.view_users()
        print("\n--- PASSENGER RECORDS ---")
        if not users:
            print("No passengers registered.")
            return
        for user in users:
            print(f"ID: {user['id']} \nName: {user['name']} \nEmail: {user['email']} \nWallet Balance: {user['wallet']} \n")

    @check_authentication
    @role_allowed(ROLE_ADMIN)
    def view_operators(self):
        operators = self.admin_service.view_operators()
        print("\n--- OPERATOR RECORDS ---")
        if not operators:
            print("No operators registered.")
            return
        for operator in operators:
            print(f"ID: {operator['id']} \nOperator Name: {operator['name']} \nEmail: {operator['email']} \n")

    @check_authentication
    @role_allowed(ROLE_ADMIN)
    def view_bookings(self):
        bookings = self.admin_service.view_all_bookings()
        print("\n--- BOOKING RECORDS ---")
        if not bookings:
            print("No bookings found.")
            return
        for booking in bookings:
            print(f"Booking ID: {booking['booking_id']} \nPassenger Name: {booking['passenger_name']} \nBus Name: {booking['bus_name']} \nRoute: {booking['origin']} -> {booking['destination']} \nBill: {booking['total_price']} \nTotal Seats Booked: {booking['seat_count']} \nStatus: {booking['status']} \n")
            
    @check_authentication
    @role_allowed(ROLE_ADMIN)
    def show_dashboard(self):
        stats = self.admin_service.get_dashboard_stats()
        print("\n====== ADMIN STATS ======")
        print(f"Total Passengers: {stats['passengers']}")
        print(f"Total Operators: {stats['operators']}")
        print(f"Total Bookings: {stats['bookings']}")