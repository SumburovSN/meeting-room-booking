from app.models.room import Room
from app.repositories.room_repository import RoomRepository
from app.services.exceptions import (
    RoomAlreadyExistsError,
    RoomNotFoundError,
)


class RoomService:
    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def create(self, name: str) -> Room:
        if self.repository.get_by_name(name):
            raise RoomAlreadyExistsError()

        room = Room(name=name)
        return self.repository.create(room)

    def get_by_id(self, room_id: int) -> Room:
        room = self.repository.get_by_id(room_id)

        if room is None:
            raise RoomNotFoundError()
        return room

    def get_all(self) -> list[Room]:
        return self.repository.get_all()

    def update(self, room: Room, name: str | None) -> Room:
        if name is not None:
            existing = self.repository.get_by_name(name)
            if existing is not None and existing.id != room.id:
                raise RoomAlreadyExistsError()

            room.name = name
        return self.repository.update(room)

    def delete(self, room: Room) -> None:
        self.repository.delete(room)
