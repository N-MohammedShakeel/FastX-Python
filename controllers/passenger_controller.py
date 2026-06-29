from services.passenger_service import PassengerService
from utils.decorators import check_authentication, role_allowed

ROLE_PASSENGER = "PASSENGER"

class PassengerController:
    def __init__(self):
        self.passenger_service = PassengerService()

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def view_buses(self):
        buses = self.passenger_service.view_all_buses()
        print("\n=== BUS RECORDS ===")
        if not buses:
            print("No buses available.")
            return
        for bus in buses:
            print(f"Bus ID: {bus['id']} \nBus Name: {bus['bus_name']} \nRoute: {bus['origin']} -> {bus['destination']} \nSeats Available: {bus['available_seats']}/{bus['total_seats']} \nDeparture Date: {bus['journey_date']} \nDeparture Time: {bus['departure_time']}\n\n")

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def search_buses(self, origin, destination, date):
        buses = self.passenger_service.search_buses(origin.lower(), destination.lower(), date)
        print("\n=== BUS RECORDS BY ROUTE AND DATE ===")
        if not buses:
            print("No buses found for the selected route and date.")
            return
        for bus in buses:
            print(f"Bus ID: {bus['id']} \nBus Name: {bus['bus_name']} \nTime: {bus['departure_time']} \nSeats Available: {bus['available_seats']}\n\n")

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def book_ticket(self, passenger_id, bus_id, seat_str):
        try:
            seat_list = [int(seat.strip()) for seat in seat_str.split(",") if seat.strip()]
            if self.passenger_service.book_ticket(passenger_id, bus_id, seat_list):
                print("SUCCESS: Ticket Booked Successfully.")
        except Exception as exception:
            print(f"ERROR: Booking Failed: {exception}")

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def cancel_booking(self, passenger_id, booking_id):
        
        try:
            if self.passenger_service.cancel_booking(passenger_id, booking_id):
                print("SUCCESS: Booking Cancelled Successfully.")
        except Exception as exception:
            print(f"ERROR: Cancellation Failed: {exception}")

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def add_money(self, passenger_id, amount):
        if amount <= 0:
            print("ERROR: Amount should be positive.")
            return
        try:
            if self.passenger_service.add_money(passenger_id, amount):
             print(f"SUCCESS: Updated Balance. Current: {self.passenger_service.get_wallet(passenger_id)}")
        except Exception as exception:
            print(f"ERROR: Deposit Failed: {exception}")

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def view_wallet(self, passenger_id):
        print(f"\nWallet: {self.passenger_service.get_wallet(passenger_id)}")

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def view_bookings(self, passenger_id):
        bookings = self.passenger_service.view_my_bookings(passenger_id)
        print("\n=== MY BOOKINGS ===")
        if not bookings:
            print("You have not booked any tickets yet.")
            return
        for booking in bookings:
            print(f"Booking ID: {booking['booking_id']} \nBus Name: {booking['bus_name']} \nRoute: {booking['origin']}->{booking['destination']} \nTotal Price: {booking['total_price']} \nSeats: {booking['seat_count']} \nStatus: {booking['status']}\n\n")

    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def view_available_seats(self, bus_id):

        layout = self.passenger_service.get_seat_layout(bus_id)

        print("\n========== SEAT LAYOUT ==========")
        print("Seat Number = Available")
        print("-- = Booked\n")

        for i in range(0, len(layout), 5):
            print("   ".join(layout[i:i+5]))

        print()
            
    @check_authentication
    @role_allowed(ROLE_PASSENGER)
    def show_dashboard(self, passenger_id, passenger_name):
        
        try:
            stats = self.passenger_service.get_dashboard_stats(passenger_id)
        except Exception as exception:
            print(f"ERROR: {exception}")
            return

        print("\n====== PASSENGER STATS ======")
        print(f"Welcome, {passenger_name}")
        print(f"Wallet Balance: {stats['wallet']}")
        print(f"Total Bookings: {stats['bookings']}")
        print(f"Total Cancellations: {stats['cancellations']}")