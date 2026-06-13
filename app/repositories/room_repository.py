from sqlalchemy.orm import Session
from app.models.room import Room


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, room: Room) -> Room:
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def get_by_id(self, room_id: int) -> Room | None:
        return (
            self.db.query(Room)
            .filter(Room.id == room_id)
            .first()
        )

    def get_by_name(self, name: str) -> Room | None:
        return (
            self.db.query(Room)
            .filter(Room.name == name)
            .first()
        )

    def get_all(self) -> list[Room]:
        return (
            self.db.query(Room)
            .order_by(Room.id)
            .all()
        )

    def update(self, room: Room) -> Room:
        self.db.commit()
        self.db.refresh(room)
        return room

    def delete(self, room: Room) -> None:
        self.db.delete(room)
        self.db.commit()