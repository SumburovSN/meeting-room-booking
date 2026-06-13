from datetime import time
from unittest.mock import Mock
import pytest
from app.models.time_slot import TimeSlot
from app.services.exceptions import (
    InvalidTimeSlotError,
    RoomNotFoundError,
    TimeSlotNotFoundError,
    TimeSlotOverlapError,
)
from app.services.time_slot_service import TimeSlotService


@pytest.fixture
def slot_repository():
    return Mock()


@pytest.fixture
def room_repository():
    return Mock()


@pytest.fixture
def service(slot_repository, room_repository):
    return TimeSlotService(
        slot_repository=slot_repository,
        room_repository=room_repository,
    )


def test_create_slot_success(
    service,
    slot_repository,
    room_repository,
):
    room_repository.get_by_id.return_value = Mock()

    created_slot = TimeSlot(
        id=1,
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    slot_repository.get_by_room.return_value = []
    slot_repository.create.return_value = created_slot

    result = service.create_slot(
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    assert result == created_slot

    room_repository.get_by_id.assert_called_once_with(1)
    slot_repository.create.assert_called_once()


def test_create_slot_invalid_equal_time(
    service,
):
    with pytest.raises(InvalidTimeSlotError):
        service.create_slot(
            room_id=1,
            start_time=time(9, 0),
            end_time=time(9, 0),
        )


def test_create_slot_invalid_reverse_time(
    service,
):
    with pytest.raises(InvalidTimeSlotError):
        service.create_slot(
            room_id=1,
            start_time=time(11, 0),
            end_time=time(9, 0),
        )


def test_create_slot_room_not_found(
    service,
    room_repository,
):
    room_repository.get_by_id.return_value = None

    with pytest.raises(RoomNotFoundError):
        service.create_slot(
            room_id=1,
            start_time=time(9, 0),
            end_time=time(11, 0),
        )


def test_create_slot_overlap(
    service,
    slot_repository,
    room_repository,
):
    room_repository.get_by_id.return_value = Mock()

    existing_slot = TimeSlot(
        id=1,
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    slot_repository.get_by_room.return_value = [existing_slot]

    with pytest.raises(TimeSlotOverlapError):
        service.create_slot(
            room_id=1,
            start_time=time(10, 0),
            end_time=time(12, 0),
        )


def test_update_slot_success(
    service,
    slot_repository,
):
    slot = TimeSlot(
        id=1,
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    slot_repository.get_by_id.return_value = slot
    slot_repository.get_by_room.return_value = [slot]
    slot_repository.update.return_value = slot

    result = service.update_slot(
        slot_id=1,
        start_time=time(9, 0),
        end_time=time(10, 0),
    )

    assert result == slot
    assert slot.start_time == time(9, 0)
    assert slot.end_time == time(10, 0)

    slot_repository.update.assert_called_once_with(slot)


def test_update_slot_not_found(
    service,
    slot_repository,
):
    slot_repository.get_by_id.return_value = None

    with pytest.raises(TimeSlotNotFoundError):
        service.update_slot(
            slot_id=1,
            start_time=time(9, 0),
            end_time=time(10, 0),
        )


def test_update_slot_invalid_time(
    service,
    slot_repository,
):
    slot = TimeSlot(
        id=1,
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    slot_repository.get_by_id.return_value = slot

    with pytest.raises(InvalidTimeSlotError):
        service.update_slot(
            slot_id=1,
            start_time=time(11, 0),
            end_time=time(10, 0),
        )


def test_update_slot_overlap_with_another_slot(
    service,
    slot_repository,
):
    slot_to_update = TimeSlot(
        id=2,
        room_id=1,
        start_time=time(12, 0),
        end_time=time(14, 0),
    )

    existing_slot = TimeSlot(
        id=1,
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    slot_repository.get_by_id.return_value = slot_to_update
    slot_repository.get_by_room.return_value = [
        existing_slot,
        slot_to_update,
    ]

    with pytest.raises(TimeSlotOverlapError):
        service.update_slot(
            slot_id=2,
            start_time=time(10, 0),
            end_time=time(13, 0),
        )


def test_update_slot_same_interval_no_overlap_with_self(
    service,
    slot_repository,
):
    slot = TimeSlot(
        id=1,
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    slot_repository.get_by_id.return_value = slot
    slot_repository.get_by_room.return_value = [slot]
    slot_repository.update.return_value = slot

    result = service.update_slot(
        slot_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    assert result == slot

    slot_repository.update.assert_called_once_with(slot)


def test_delete_slot_success(
    service,
    slot_repository,
):
    slot = TimeSlot(
        id=1,
        room_id=1,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    slot_repository.get_by_id.return_value = slot

    service.delete_slot(1)

    slot_repository.delete.assert_called_once_with(slot)


def test_delete_slot_not_found(
    service,
    slot_repository,
):
    slot_repository.get_by_id.return_value = None

    with pytest.raises(TimeSlotNotFoundError):
        service.delete_slot(1)


def test_get_slots_by_room_id_success(
    service,
    slot_repository,
    room_repository,
):
    room_repository.get_by_id.return_value = Mock()

    slots = [
        TimeSlot(
            id=1,
            room_id=1,
            start_time=time(9, 0),
            end_time=time(11, 0),
        ),
        TimeSlot(
            id=2,
            room_id=1,
            start_time=time(11, 0),
            end_time=time(13, 0),
        ),
    ]

    slot_repository.get_by_room.return_value = slots

    result = service.get_slots_by_room_id(1)

    assert result == slots

    room_repository.get_by_id.assert_called_once_with(1)
    slot_repository.get_by_room.assert_called_once_with(1)


def test_get_slots_by_room_id_room_not_found(
    service,
    room_repository,
):
    room_repository.get_by_id.return_value = None

    with pytest.raises(RoomNotFoundError):
        service.get_slots_by_room_id(1)