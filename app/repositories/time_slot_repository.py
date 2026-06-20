from datetime import time
from sqlalchemy.orm import Session
from app.models.time_slot import TimeSlot


class TimeSlotRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_room(self, room_id: int) -> list[TimeSlot]:
        return (
            self.db.query(TimeSlot)
            .filter(TimeSlot.room_id == room_id)
            .order_by(TimeSlot.start_time)
            .all()
        )

    def get_all(self) -> list[TimeSlot]:
        return self.db.query(TimeSlot).order_by(TimeSlot.room_id, TimeSlot.start_time).all()

    def get_by_room_and_time(self, room_id: int, start_time: time, end_time: time) -> TimeSlot | None:
        return (
            self.db.query(TimeSlot)
            .filter(
                TimeSlot.room_id == room_id,
                TimeSlot.start_time == start_time,
                TimeSlot.end_time == end_time,
            )
            .first()
        )

    def get_by_id(self, time_slot_id: int) -> TimeSlot | None:
        return (
            self.db.query(TimeSlot)
            .filter(TimeSlot.id == time_slot_id)
            .first()
        )

    def create(self, slot: TimeSlot) -> TimeSlot:
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def update(self, slot: TimeSlot) -> TimeSlot:
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def delete(self, slot: TimeSlot) -> None:
        self.db.delete(slot)
        self.db.commit()
