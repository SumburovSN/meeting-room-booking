from datetime import date, time
from unittest.mock import Mock, patch
import pytest
from app.models.booking import Booking
from app.services.booking_service import BookingService
from app.services.exceptions import (
    BookingNotFoundError,
    SlotAlreadyBookedError,
    InvalidRoomTimeSlotError,
    UserNotFoundError,
    RoomNotFoundError,
    InvalidBookingDateError,
)


@pytest.fixture
def booking_repository():
    return Mock()


@pytest.fixture
def room_repository():
    return Mock()


@pytest.fixture
def time_slot_repository():
    return Mock()


@pytest.fixture
def user_repository():
    return Mock()


@pytest.fixture
def service(
    booking_repository,
    room_repository,
    time_slot_repository,
    user_repository,
):
    return BookingService(
        booking_repository=booking_repository,
        room_repository=room_repository,
        time_slot_repository=time_slot_repository,
        user_repository=user_repository,
    )


# =========================
# get_by_id
# =========================

def test_get_by_id_success(service, booking_repository):
    booking = Mock(spec=Booking)

    booking_repository.get_by_id.return_value = booking

    result = service.get_by_id(1)

    assert result == booking
    booking_repository.get_by_id.assert_called_once_with(1)


def test_get_by_id_not_found(service, booking_repository):
    booking_repository.get_by_id.return_value = None

    with pytest.raises(BookingNotFoundError):
        service.get_by_id(1)


# =========================
# get_all
# =========================

def test_get_all(service, booking_repository):
    bookings = [Mock(spec=Booking), Mock(spec=Booking)]

    booking_repository.get_all.return_value = bookings

    result = service.get_all()

    assert result == bookings
    booking_repository.get_all.assert_called_once()


# =========================
# get_by_user
# =========================

def test_get_by_user(service, booking_repository):
    bookings = [Mock(spec=Booking)]

    booking_repository.get_by_user.return_value = bookings

    result = service.get_by_user(1)

    assert result == bookings
    booking_repository.get_by_user.assert_called_once_with(1)


# =========================
# create_booking
# =========================
@patch("app.services.booking_service.datetime")
def test_create_booking_success(
    mock_datetime,
    service,
    user_repository,
    room_repository,
    time_slot_repository,
    booking_repository,
):
    mock_datetime.now.return_value.time.return_value = time(10, 0)

    user_repository.get_by_id.return_value = Mock(is_active=True)

    room_repository.get_by_id.return_value = Mock()

    time_slot_repository.get_by_id.return_value = Mock(
        room_id=1,
        end_time=time(18, 0),
    )

    booking_repository.get_by_room_slot_date.return_value = None

    created_booking = Mock(spec=Booking)
    booking_repository.create.return_value = created_booking

    result = service.create_booking(
        user_id=1,
        room_id=1,
        time_slot_id=1,
        booking_date=date.today(),
    )

    assert result == created_booking
    booking_repository.create.assert_called_once()


def test_create_booking_user_not_found(
    service,
    user_repository,
):
    user_repository.get_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        service.create_booking(
            1,
            1,
            1,
            date.today(),
        )


def test_create_booking_user_inactive(
    service,
    user_repository,
):
    user_repository.get_by_id.return_value = Mock(
        is_active=False
    )

    with pytest.raises(UserNotFoundError):
        service.create_booking(
            1,
            1,
            1,
            date.today(),
        )


def test_create_booking_past_date(
    service,
    user_repository,
):
    user_repository.get_by_id.return_value = Mock(
        is_active=True
    )

    with pytest.raises(InvalidBookingDateError):
        service.create_booking(
            1,
            1,
            1,
            date(2000, 1, 1),
        )


def test_create_booking_room_not_found(
    service,
    user_repository,
    room_repository,
):
    user_repository.get_by_id.return_value = Mock(
        is_active=True
    )

    room_repository.get_by_id.return_value = None

    with pytest.raises(RoomNotFoundError):
        service.create_booking(
            1,
            1,
            1,
            date.today(),
        )


def test_create_booking_slot_not_found(
    service,
    user_repository,
    room_repository,
    time_slot_repository,
):
    user_repository.get_by_id.return_value = Mock(
        is_active=True
    )

    room_repository.get_by_id.return_value = Mock()

    time_slot_repository.get_by_id.return_value = None

    with pytest.raises(InvalidRoomTimeSlotError):
        service.create_booking(
            1,
            1,
            1,
            date.today(),
        )


def test_create_booking_slot_belongs_to_other_room(
    service,
    user_repository,
    room_repository,
    time_slot_repository,
):
    user_repository.get_by_id.return_value = Mock(
        is_active=True
    )

    room_repository.get_by_id.return_value = Mock()

    time_slot_repository.get_by_id.return_value = Mock(
        room_id=999,
        end_time=time(18, 0),
    )

    with pytest.raises(InvalidRoomTimeSlotError):
        service.create_booking(
            1,
            1,
            1,
            date.today(),
        )


@patch("app.services.booking_service.datetime")
def test_create_booking_slot_already_finished_today(
    mock_datetime,
    service,
    user_repository,
    room_repository,
    time_slot_repository,
):
    mock_datetime.now.return_value.time.return_value = time(
        15,
        0,
    )

    user_repository.get_by_id.return_value = Mock(
        is_active=True
    )

    room_repository.get_by_id.return_value = Mock()

    time_slot_repository.get_by_id.return_value = Mock(
        room_id=1,
        end_time=time(14, 0),
    )

    with pytest.raises(InvalidBookingDateError):
        service.create_booking(
            1,
            1,
            1,
            date.today(),
        )


@patch("app.services.booking_service.datetime")
def test_create_booking_slot_already_booked(
    mock_datetime,
    service,
    user_repository,
    room_repository,
    time_slot_repository,
    booking_repository,
):
    mock_datetime.now.return_value.time.return_value = time(10, 0)
    user_repository.get_by_id.return_value = Mock(
        is_active=True
    )

    room_repository.get_by_id.return_value = Mock()

    time_slot_repository.get_by_id.return_value = Mock(
        room_id=1,
        end_time=time(18, 0),
    )

    booking_repository.get_by_room_slot_date.return_value = Mock()

    with pytest.raises(SlotAlreadyBookedError):
        service.create_booking(
            1,
            1,
            1,
            date.today(),
        )


# =========================
# delete_booking
# =========================

def test_delete_booking_success(
    service,
    booking_repository,
):
    booking = Mock(spec=Booking)

    booking_repository.get_by_id.return_value = booking

    service.delete_booking(1)

    booking_repository.delete.assert_called_once_with(
        booking
    )


def test_delete_booking_not_found(
    service,
    booking_repository,
):
    booking_repository.get_by_id.return_value = None

    with pytest.raises(BookingNotFoundError):
        service.delete_booking(1)


# =========================
# get_availability
# =========================

def test_get_availability(
    service,
    booking_repository,
    room_repository,
    time_slot_repository,
):
    booking_repository.get_by_date.return_value = [
        Mock(time_slot_id=1)
    ]

    slot1 = Mock(
        id=1,
        room_id=10,
        start_time=time(9, 0),
        end_time=time(10, 0),
    )

    slot2 = Mock(
        id=2,
        room_id=10,
        start_time=time(10, 0),
        end_time=time(11, 0),
    )

    time_slot_repository.get_all.return_value = [
        slot1,
        slot2,
    ]

    room = Mock()
    room.id = 10
    room.name = "Room A"

    room_repository.get_by_id.return_value = room

    result = service.get_availability(
        date(2026, 6, 17)
    )

    assert len(result) == 2

    assert result[0] == {
        "room_id": 10,
        "room_name": "Room A",
        "time_slot_id": 1,
        "start_time": time(9, 0),
        "end_time": time(10, 0),
        "is_available": False,
    }

    assert result[1] == {
        "room_id": 10,
        "room_name": "Room A",
        "time_slot_id": 2,
        "start_time": time(10, 0),
        "end_time": time(11, 0),
        "is_available": True,
    }

    booking_repository.get_by_date.assert_called_once_with(
        date(2026, 6, 17)
    )

    time_slot_repository.get_all.assert_called_once()

    assert room_repository.get_by_id.call_count == 2


def test_get_availability_no_bookings(
    service,
    booking_repository,
    room_repository,
    time_slot_repository,
):
    booking_repository.get_by_date.return_value = []

    slot = Mock(
        id=1,
        room_id=10,
        start_time=time(9, 0),
        end_time=time(10, 0),
    )

    time_slot_repository.get_all.return_value = [slot]

    room_repository.get_by_id.return_value = Mock(
        id=10,
        name="Room A",
    )

    result = service.get_availability(
        date(2026, 6, 17)
    )

    assert len(result) == 1
    assert result[0]["is_available"] is True
