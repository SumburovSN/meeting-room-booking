from datetime import time
from app.models import TimeSlot
from app.repositories.room_repository import RoomRepository
from app.repositories.time_slot_repository import TimeSlotRepository
from app.services.exceptions import TimeSlotOverlapError, InvalidTimeSlotError, TimeSlotNotFoundError, RoomNotFoundError


class TimeSlotService:
    def __init__(self, slot_repository: TimeSlotRepository, room_repository: RoomRepository):
        self.slot_repository = slot_repository
        self.room_repository = room_repository

    def _validate_no_overlap(self, room_id: int, start_time: time, end_time: time, exclude_slot_id: int | None = None):
        slots = self.slot_repository.get_by_room(room_id)
        for slot in slots:
            if exclude_slot_id is not None and slot.id == exclude_slot_id:
                continue
            if start_time < slot.end_time and end_time > slot.start_time:
                raise TimeSlotOverlapError()

    def create_slot(self, room_id: int, start_time: time, end_time: time):
        if start_time >= end_time:
            raise InvalidTimeSlotError()

        room = self.room_repository.get_by_id(room_id)
        if room is None:
            raise RoomNotFoundError()

        self._validate_no_overlap(room_id, start_time, end_time)

        slot = TimeSlot(room_id=room_id, start_time=start_time, end_time=end_time)
        return self.slot_repository.create(slot)

    def update_slot(self, slot_id: int, start_time: time, end_time: time):
        slot = self.slot_repository.get_by_id(slot_id)
        if slot is None:
            raise TimeSlotNotFoundError()

        if start_time >= end_time:
            raise InvalidTimeSlotError()

        self._validate_no_overlap(slot.room_id, start_time, end_time, exclude_slot_id=slot.id)

        slot.start_time = start_time
        slot.end_time = end_time
        return self.slot_repository.update(slot)

    def delete_slot(self, slot_id: int):
        slot = self.slot_repository.get_by_id(slot_id)
        if slot is None:
            raise TimeSlotNotFoundError()
        self.slot_repository.delete(slot)

    def get_slots_by_room_id(self, room_id: int) -> list[TimeSlot]:
        room = self.room_repository.get_by_id(room_id)
        if room is None:
            raise RoomNotFoundError()
        return self.slot_repository.get_by_room(room_id)
