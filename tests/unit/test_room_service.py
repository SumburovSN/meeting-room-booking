from unittest.mock import Mock
import pytest
from app.models.room import Room
from app.services.room_service import RoomService
from app.services.exceptions import (
    RoomAlreadyExistsError,
    RoomNotFoundError,
)


@pytest.fixture
def repository():
    return Mock()


@pytest.fixture
def service(repository):
    return RoomService(repository)


def test_create_room_success(
    service,
    repository,
):
    room = Room(name="Conference Room")

    repository.get_by_name.return_value = None
    repository.create.return_value = room

    result = service.create("Conference Room")

    assert result == room

    repository.get_by_name.assert_called_once_with(
        "Conference Room"
    )

    repository.create.assert_called_once()


def test_create_room_already_exists(
    service,
    repository,
):
    repository.get_by_name.return_value = Mock()

    with pytest.raises(RoomAlreadyExistsError):
        service.create("Conference Room")


def test_get_by_id_success(
    service,
    repository,
):
    room = Room(
        id=1,
        name="Conference Room",
    )

    repository.get_by_id.return_value = room

    result = service.get_by_id(1)

    assert result == room

    repository.get_by_id.assert_called_once_with(1)


def test_get_by_id_not_found(
    service,
    repository,
):
    repository.get_by_id.return_value = None

    with pytest.raises(RoomNotFoundError):
        service.get_by_id(1)


def test_get_all(
    service,
    repository,
):
    rooms = [
        Room(id=1, name="Room 1"),
        Room(id=2, name="Room 2"),
    ]

    repository.get_all.return_value = rooms

    result = service.get_all()

    assert result == rooms

    repository.get_all.assert_called_once()


def test_update_room_name_success(
    service,
    repository,
):
    room = Room(
        id=1,
        name="Old Name",
    )

    repository.get_by_name.return_value = None
    repository.update.return_value = room

    result = service.update(
        room=room,
        name="New Name",
    )

    assert result == room
    assert room.name == "New Name"

    repository.update.assert_called_once_with(room)


def test_update_room_duplicate_name(
    service,
    repository,
):
    room = Room(
        id=1,
        name="Old Name",
    )

    existing_room = Room(
        id=2,
        name="New Name",
    )

    repository.get_by_name.return_value = existing_room

    with pytest.raises(RoomAlreadyExistsError):
        service.update(
            room=room,
            name="New Name",
        )


def test_update_room_same_name_for_same_room(
    service,
    repository,
):
    room = Room(
        id=1,
        name="Conference Room",
    )

    repository.get_by_name.return_value = room
    repository.update.return_value = room

    result = service.update(
        room=room,
        name="Conference Room",
    )

    assert result == room

    repository.update.assert_called_once_with(room)


def test_update_room_without_name_change(
    service,
    repository,
):
    room = Room(
        id=1,
        name="Conference Room",
    )

    repository.update.return_value = room

    result = service.update(
        room=room,
        name=None,
    )

    assert result == room

    repository.update.assert_called_once_with(room)


def test_delete_room(
    service,
    repository,
):
    room = Room(
        id=1,
        name="Conference Room",
    )

    service.delete(room)

    repository.delete.assert_called_once_with(room)
