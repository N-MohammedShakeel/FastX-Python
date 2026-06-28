from controllers.auth_controller import AuthController
from controllers.passenger_controller import PassengerController
from controllers.operator_controller import OperatorController
from controllers.admin_controller import AdminController

auth_controller = AuthController()
passenger_controller = PassengerController()
operator_controller = OperatorController()
admin_controller = AdminController()

CURRENT_USER = None
ROLE_PASSENGER = "PASSENGER"
ROLE_OPERATOR = "OPERATOR"
ROLE_ADMIN = "ADMIN"

def show_passenger_menu():
    global CURRENT_USER

    while CURRENT_USER:

        passenger_controller.show_dashboard(CURRENT_USER.id, CURRENT_USER.name)

        print("\n--- PASSENGER DASHBOARD ---")
        print("1. View Available Buses")
        print("2. Search Buses By Route")
        print("3. Book Tickets")
        print("4. Cancel Booking")
        print("5. Add Money to Wallet")
        print("6. View My Bookings")
        print("7. Logout")
        
        try:
            choice = int(input("Enter your choice: "))

            match choice:
                case 1: 
                    passenger_controller.view_buses()

                case 2:
                    origin = input("Enter Origin Location: ").strip()
                    destination = input("Enter Destination Location: ").strip()
                    date_to_depart = input("Enter journey Date (YYYY-MM-DD): ").strip()
                    passenger_controller.search_buses(origin, destination, date_to_depart)

                case 3:
                    bus_id = int(input("Enter Bus ID: "))
                    try:
                        passenger_controller.view_available_seats(bus_id)
                        seats = input("Enter seats number (comma separated, e.g., 2,3,6): ").strip()
                        passenger_controller.book_ticket(CURRENT_USER.id, bus_id, seats)
                    except Exception as exception:
                        print(f"ERROR: Booking Failed: {exception}")

                case 4:
                    booking_id = int(input("Enter booking ID: "))
                    passenger_controller.cancel_booking(CURRENT_USER.id, booking_id)

                case 5:
                    amount_to_deposit = float(input("Deposit Value: "))
                    passenger_controller.add_money(CURRENT_USER.id, amount_to_deposit)

                case 6: 
                    passenger_controller.view_bookings(CURRENT_USER.id)

                case 7:
                    auth_controller.logout(CURRENT_USER.email)
                    CURRENT_USER = None
                    print("\nLogout successful.")
                    break

                case _: 
                    print("\nInvalid choice.")

        except ValueError:
            print("[ERROR] Invalid Input. Please try again.")

def show_operator_menu():
    global CURRENT_USER

    while CURRENT_USER:

        operator_controller.show_dashboard(CURRENT_USER.id, CURRENT_USER.name)

        print("\n--- OPERATOR DASHBOARD ---")
        print("1. Register New Bus")
        print("2. Update Bus")
        print("3. Delete Bus")
        print("4. View All Buses")
        print("5. View Passenger Bookings")
        print("6. Logout")

        try:
            choice = int(input("Enter your choice: "))

            match choice:

                case 1:
                    bus_name = input("Enter Bus Name: ").strip()
                    origin = input("Enter Origin Location:: ").strip()
                    destination = input("Enter Destination Location:: ").strip()
                    date_to_depart = input("Departure Date (YYYY-MM-DD): ").strip()
                    time_to_depart = input("Departure Time (HH:MM:SS): ").strip()
                    total_seats = int(input("Total seat capacity: "))
                    price_per_ticket = float(input("Price per ticket (in Rupees): "))
                    operator_controller.add_bus(bus_name, origin, destination, date_to_depart, time_to_depart, total_seats, CURRENT_USER.id, price_per_ticket)

                case 2:
                    bus_id = int(input("Enter Bus ID: "))
                    bus_name = input("Enter new Bus Name: ").strip()
                    origin = input("Enter new Origin Location:: ").strip()
                    destination = input("Enter new Destination Location:: ").strip()
                    date_to_depart = input("New Departure Date (YYYY-MM-DD): ").strip()
                    time_to_depart = input("New Departure Time (HH:MM:SS): ").strip()
                    price_per_ticket = float(input("Update Price per ticket (in Rupees): "))
                    operator_controller.update_bus(bus_id, CURRENT_USER.id, bus_name, origin, destination, date_to_depart, time_to_depart, price_per_ticket)

                case 3:
                    bus_id = int(input("Enter Bus ID: "))
                    operator_controller.delete_bus(bus_id, CURRENT_USER.id)

                case 4: 
                    operator_controller.view_fleet(CURRENT_USER.id)

                case 5: 
                    operator_controller.view_bookings(CURRENT_USER.id)

                case 6:
                    auth_controller.logout(CURRENT_USER.email)
                    CURRENT_USER = None
                    print("\nLogout successful.")
                    break

                case _: 
                    print("\nInvalid choice.")

        except ValueError:
            print("[ERROR] Invalid Input. Please try again.")

def show_admin_menu():
    global CURRENT_USER

    while CURRENT_USER:

        admin_controller.show_dashboard()

        print("\n--- ADMIN DASHBOARD ---")
        print("1. View all Passengers")
        print("2. View all Operators")
        print("3. View all Bookings")
        print("4. Logout")

        try:
            choice = int(input("Enter your choice: "))

            match choice:

                case 1: 
                    admin_controller.view_passengers()
                case 2: 
                    admin_controller.view_operators()
                case 3: 
                    admin_controller.view_bookings()
                case 4:
                    auth_controller.logout(CURRENT_USER.email)
                    CURRENT_USER = None
                    print("\nLogout successful.")
                    break
                case _:
                    print("\nInvalid choice.")

        except ValueError:
            print("[ERROR] Invalid Input. Please try again.")

def route_dashboard():
    global CURRENT_USER

    if not CURRENT_USER: 
        return
    if CURRENT_USER.role == ROLE_PASSENGER: 
        show_passenger_menu()
    elif CURRENT_USER.role == ROLE_OPERATOR: 
        show_operator_menu()
    elif CURRENT_USER.role == ROLE_ADMIN: 
        show_admin_menu()

if __name__ == "__main__":
    print("--------------Welcome to FastX--------------")

    auto_user = auth_controller.get_auto_session()
    if auto_user:
        CURRENT_USER = auto_user
        print(f"\n[SESSION AUTO LOGIN] Welcome back: {CURRENT_USER.email}")
        route_dashboard()

    while True:

        print("\n========== FastX ==========")
        print("1. Login")
        print("2. Register Passenger")
        print("3. Register Operator")
        print("4. Exit")

        try:

            choice = int(input("Enter your choice: "))

            match choice:

                case 1:
                    email = input("Enter your Email: ").strip()
                    password = input("Enter your Password: ").strip()
                    logged_user = auth_controller.login(email, password)
                    if logged_user:
                        CURRENT_USER = logged_user
                        route_dashboard()

                case 2:
                    passenger_name = input("Enter your Name: ").strip()
                    email = input("Enter your Email: ").strip()
                    password = input("Enter your Password: ").strip()
                    auth_controller.register_passenger(passenger_name, email, password)

                case 3:
                    operator_name = input("Enter your Name: ").strip()
                    email = input("Enter your Email: ").strip()
                    password = input("Enter your Password: ").strip()
                    auth_controller.register_operator(operator_name, email, password)

                case 4:
                    print("\nExiting Application......\nThank you for using FastX.")
                    break

                case _: 
                    print("Selection pointer out of range.")

        except ValueError:
            print("[ERROR] Value typing verification rejected.")