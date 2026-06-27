import sys
from services.auth_service import AuthService
from services.passenger_service import PassengerService
from services.operator_service import OperatorService
from services.admin_service import AdminService
from utils.validators import is_valid_email, is_valid_password

auth_service = AuthService()
passenger_service = PassengerService()
operator_service = OperatorService()
admin_service = AdminService()

CURRENT_USER = None
ROLE_PASSENGER = "PASSENGER"
ROLE_OPERATOR = "OPERATOR"
ROLE_ADMIN = "ADMIN"

def show_passenger_menu():
    """Renders passenger capabilities interface terminal menus."""
    global CURRENT_USER
    while True:
        print(f"\n===== PASSENGER DASHBOARD ({CURRENT_USER['email']}) =====")
        print("1. View Available Buses")
        print("2. Search Buses By Route")
        print("3. Book Tickets")
        print("4. View My Booking")
        print("5. Logout")
        
        choice = int(input("Enter your choice: "))

        match(choice):

            case 1:
                buses = passenger_service.view_all_buses()
                print("\n--- Available Buses ---")
                for bus in buses:
                    print(f"ID: {bus['id']} | {bus['bus_name']} | Route: {bus['source']} -> {bus['destination']} | Date: {bus['journey_date']} | Time: {bus['departure_time']} | Available Seats: {bus['available_seats']}/{bus['total_seats']}")
                    
            case 2:
                src = input("Enter Origin Location: ").strip()
                dest = input("Enter Destination Location: ").strip()
                date_str = input("Journey Target Date (YYYY-MM-DD): ").strip()
                
                buses = passenger_service.search_buses(src, dest, date_str)
                print("\n--- MATCHING TRIP ROUTES ---")
                for bus in buses:
                    print(f"ID: {bus['id']} | {bus['bus_name']} | Time: {bus['departure_time']} | Available Seats: {bus['available_seats']}")
                    
            case 3:
                try:
                    bus_id = int(input("Enter Bus ID: "))
                    seats = int(input("Number Of Seats To Book: "))
                    if seats <= 0:
                        print("[ERROR] Invalid quantity.")
                        continue
                        
                    success = passenger_service.book_ticket(CURRENT_USER["id"], bus_id, seats)
                    if success:
                        print("\n[SUCCESS] Tickets booked successfully!")
                    else:
                        print("\n[ERROR] Failed to book tickets. Please try again.")
                except ValueError:
                    print("[ERROR] Invalid input.")
                    
            case 4:
                bookings = passenger_service.get_my_bookings(CURRENT_USER["id"])
                print("\n--- MY BOOKINGS ---")
                for booking in bookings:
                    print(f"Booking ID: {booking['booking_id']} | Fleet: {booking['bus_name']} | Route: {booking['source']}->{booking['destination']} | Date: {booking['journey_date']} | Booked Seats: {booking['seat_count']} (Confirmed On: {booking['booking_date']})")
                    
            case 5:
                auth_service.logout()
                CURRENT_USER = None
                print("\nLogout successful.")
                break

            case _:
                print("\nInvalid choice.")

def show_operator_menu():
    """Renders dynamic vendor interaction dashboard structures."""
    global CURRENT_USER
    while True:
        print(f"\n===== OPERATOR DASHBOARD ({CURRENT_USER['email']}) =====")
        print("1. Register New Bus")
        print("2. View your Fleet")
        print("3. Delete Bus")
        print("4. View Passenger Bookings")
        print("5. Logout")
        
        choice = int(input("Enter your choice: "))

        match(choice):
        
            case 1:
                name = input("Enter Bus Name: ").strip()
                src = input("Enter Origin Location: ").strip()
                dest = input("Enter Destination Location: ").strip()
                date_str = input("Travel Schedule Date (YYYY-MM-DD): ").strip()
                time_str = input("Departure Timeline Hour (HH:MM:SS): ").strip()
                try:
                    total_seats = int(input("Total Seat Capacity: "))
                    
                    success = operator_service.add_bus(name, src, dest, date_str, time_str, total_seats, CURRENT_USER["id"])
                    if success:
                        print("\n[SUCCESS] Bus Registered Successfully.")
                    else:
                        print("\n[ERROR] Bus Registration Failed. Please try again.")
                except ValueError:
                    print("Invalid input.")
                    
            case 2:
                buses = operator_service.view_my_buses(CURRENT_USER["id"])
                print("\n--- MY FLEET ---")
                for bus in buses:
                    print(f"ID: {bus['id']} | {bus['bus_name']} | {bus['source']} -> {bus['destination']} | Available Seats: {bus['available_seats']}/{bus['total_seats']}")
                    
            case 3:
                try:
                    bus_id = int(input("Enter you bus ID to delete: "))
                    success = operator_service.delete_bus(bus_id, CURRENT_USER["id"])
                    if success:
                        print("\n[SUCCESS] Bus deleted successfully.")
                    else:
                        print("\n[ERROR] Bus deletion failed. Please try again.")
                except ValueError:
                    print("Invalid input.")
                    
            case 4:
                bookings = operator_service.view_bus_bookings(CURRENT_USER["id"])
                print("\n--- ALL PASSENGER BOOKINGS ---")
                for booking in bookings:
                    print(f"Ticket ID: {booking['booking_id']} | Passenger: {booking['passenger_name']} | Fleet: {booking['bus_name']} | Seats Filled: {booking['seat_count']}")
                    
            case 5:
                auth_service.logout()
                CURRENT_USER = None
                print("\nLogout successful.")
                break

            case _:
                print("\nInvalid choice.")

def show_admin_menu():
    """Renders system structural administration analytics templates."""
    global CURRENT_USER
    while True:
        print("\n===== ADMIN DASHBOARD =====")
        print("1. View all Passengers")
        print("2. View all Operators")
        print("3. View all Bookings")
        print("4. Logout")
        
        choice = int(input("Enter your choice: "))

        match(choice):
        
            case 1:
                users = admin_service.view_users()
                print("\n--- REGISTERED PASSENGERS ---")
                for user in users:
                    print(f"ID: {user['id']} | User: {user['name']} | Email: {user['email']}")
                    
            case 2:
                operators = admin_service.view_operators()
                print("\n--- REGISTERED OPERATORS ---")
                for operator in operators:
                    print(f"ID: {operator['id']} | Operator Name: {operator['name']} | Contact: {operator['email']}")
                    
            case 3:
                bookings = admin_service.view_all_bookings()
                print("\n--- ALL PASSENGER BOOKINGS ---")
                for booking in bookings:
                    print(f"Booking ID: {booking['booking_id']} | Customer: {booking['passenger_name']} | Bus: {booking['bus_name']} | Trip: {booking['source']}->{booking['destination']} | Seats Reserved: {booking['seat_count']}")
                    
            case 4:
                auth_service.logout()
                CURRENT_USER = None
                print("\nLogout successful.")
                break

            case _:
                print("\nInvalid choice.")

def routing_dashboard_router():
    """Directs user interface pipelines tracking variable status data definitions."""
    global CURRENT_USER, ROLE_PASSENGER, ROLE_OPERATOR, ROLE_ADMIN
    if not CURRENT_USER:
        return
        
    role = CURRENT_USER.get("role")
    if role == ROLE_PASSENGER:
        show_passenger_menu()
    elif role == ROLE_OPERATOR:
        show_operator_menu()
    elif role == ROLE_ADMIN:
        show_admin_menu()


"""Starts core system loops and manages initialization parameters."""

print("Welcome to FastX Terminal Systems Engine Architecture")

user = auth_service.get_auto_session()

if user:
    CURRENT_USER = user
    print(f"\n[SESSION AUTO LOGIN] Restored session for: {user['email']}")
    routing_dashboard_router()
    
while True:
    print("\n========== FastX ==========")
    print("1. Login")
    print("2. Register Passenger")
    print("3. Register Operator")
    print("4. Exit")
    
    choice = int(input("Enter your choice: "))

    match choice:
    
        case 1:
            email = input("Enter your Email: ").strip()
            password = input("Enter your Password: ").strip()
            
            logged_in_user = auth_service.login(email, password)
            if logged_in_user:
                CURRENT_USER = logged_in_user
                routing_dashboard_router()
            else:
                print("\n[ALERT] Credentials Invalid.")
                
        case 2:
            name = input("Enter your Name: ").strip()
            email = input("Enter your Email: ").strip()
            password = input("Enter your Password: ").strip()
            
            if not is_valid_email(email) or not is_valid_password(password):
                print(f"\n[WARNING] Invalid Email / Password. password min 6 chars.")
                continue
                
            if auth_service.register(name, email, password, ROLE_PASSENGER):
                print("\n[SUCCESS] Passenger details saved successfully! Proceed to Login.")
            else:
                print("\n[ERROR] Registration Failed.")
                
        case 3:
            name = input("Enter your Name: ").strip()
            email = input("Enter your Email: ").strip()
            password = input("Enter your Password: ").strip()
            
            if not is_valid_email(email) or not is_valid_password(password):
                print(f"\n[WARNING] Invalid Email / Password. password min 6 chars.")
                continue
                
            if auth_service.register(name, email, password, ROLE_OPERATOR):
                print("\n[SUCCESS] Operator details saved successfully! Proceed to Login.")
            else:
                print("\n[ERROR] Registration Failed.")
                
        case 4:
            print("\nExiting Application......\nThank you for using FastX.")
            sys.exit(0)

        case _:
            print("\nInvalid choice.")
