import pytest
from unittest.mock import MagicMock

from services.passenger_service import PassengerService
from services.operator_service import OperatorService
from utils.password_util import hash_password, verify_password

from models.user import User
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.bus_not_found_exception import BusNotFoundException


@pytest.fixture
def passenger_service():
    service = PassengerService()

    service.user_repo = MagicMock()
    service.bus_repo = MagicMock()
    service.booking_repo = MagicMock()
    service.seat_repo = MagicMock()

    return service


@pytest.fixture
def operator_service():
    service = OperatorService()

    service.bus_repo = MagicMock()
    service.booking_repo = MagicMock()
    service.user_repo = MagicMock()

    return service


def test_hash_password():
    password = "admin123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)


@pytest.mark.parametrize(
    "password,wrong_password",
    [
        ("admin123", "admin"),
        ("fastx123", "wrong"),
    ],
)
def test_verify_password_invalid(password, wrong_password):

    hashed = hash_password(password)
    assert verify_password(wrong_password, hashed) is False


def test_get_wallet_success(passenger_service):

    passenger_service.user_repo.find_by_id.return_value = User(1,"MS","ms@gmail.com","hashed","PASSENGER",1500.0)
    assert passenger_service.get_wallet(1) == 1500.0


def test_get_wallet_user_not_found(passenger_service):

    passenger_service.user_repo.find_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        passenger_service.get_wallet(1)


def test_get_seat_layout_invalid_bus(passenger_service):

    passenger_service.bus_repo.find_by_id.return_value = None

    with pytest.raises(BusNotFoundException):
        passenger_service.get_seat_layout(10)


def test_update_bus_invalid_bus(operator_service):

    operator_service.bus_repo.find_by_id.return_value = None

    with pytest.raises(BusNotFoundException):
        operator_service.update_bus(1,1,"FastX","Chennai","Bangalore","2026-07-01","08:00:00",500)