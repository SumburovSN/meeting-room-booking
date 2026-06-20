from datetime import date, time
from unittest.mock import Mock
import pytest
from app.services.availability_service import AvailabilityService
from types import SimpleNamespace


@pytest.fixture
def availability_repository():
    return Mock()


@pytest.fixture
def service(availability_repository):
    return AvailabilityService(availability_repository)


room = SimpleNamespace(id=10, name="Room A")

slot1 = SimpleNamespace(
    id=1,
    start_time=time(9, 0),
    end_time=time(10, 0),
)

slot2 = SimpleNamespace(
    id=2,
    start_time=time(10, 0),
    end_time=time(11, 0),
)


def test_get_availability(
    service,
    availability_repository,
):

    availability_repository.get_by_date.return_value = [
        (room, slot1, 1),      # забронирован текущим пользователем
        (room, slot2, None),   # свободен
    ]

    result = service.get_availability(
        date(2026, 6, 17),
        current_user_id=1,
    )

    assert len(result) == 1

    room_availability = result[0]

    assert room_availability.room_id == 10
    assert room_availability.room_name == "Room A"

    assert len(room_availability.slots) == 2

    assert room_availability.slots[0].time_slot_id == 1
    assert room_availability.slots[0].is_available is False
    assert room_availability.slots[0].booked_by_me is True

    assert room_availability.slots[1].time_slot_id == 2
    assert room_availability.slots[1].is_available is True
    assert room_availability.slots[1].booked_by_me is False

    availability_repository.get_by_date.assert_called_once_with(
        date(2026, 6, 17)
    )


def test_get_availability_no_bookings(
    service,
    availability_repository,
):

    availability_repository.get_by_date.return_value = [
        (room, slot1, None),
    ]

    result = service.get_availability(
        date(2026, 6, 17),
        current_user_id=1,
    )

    assert len(result) == 1

    room_availability = result[0]

    assert room_availability.room_id == 10
    assert room_availability.room_name == "Room A"

    assert len(room_availability.slots) == 1

    assert room_availability.slots[0].is_available is True
    assert room_availability.slots[0].booked_by_me is False
