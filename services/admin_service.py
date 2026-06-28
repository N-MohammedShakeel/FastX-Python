from repositories.user_repository import UserRepository
from repositories.booking_repository import BookingRepository
from utils.logger import log_info

ROLE_PASSENGER = "PASSENGER"
ROLE_OPERATOR = "OPERATOR"

class AdminService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.booking_repo = BookingRepository()

    def view_users(self):
        log_info("Admin viewed passenger records.")
        return self.user_repo.view_users_by_role(ROLE_PASSENGER)

    def view_operators(self):
        log_info("Admin viewed operator records.")
        return self.user_repo.view_users_by_role(ROLE_OPERATOR)

    def view_all_bookings(self):
        log_info("Admin viewed booking records.")
        return self.booking_repo.find_all_bookings_dashboard()

    def get_dashboard_stats(self):
        return {
            "passengers": self.user_repo.get_passenger_count(),
            "operators": self.user_repo.get_operator_count(),
            "bookings": self.booking_repo.count_all_bookings()
        }