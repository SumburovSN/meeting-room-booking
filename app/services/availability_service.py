from datetime import date
from app.repositories.availability_repository import AvailabilityRepository
from app.schemas.availability import AvailabilityResponse, TimeSlotAvailability


class AvailabilityService:
    def __init__(self, availability_repository: AvailabilityRepository):
        self.availability_repository = availability_repository

    def get_availability(self, booking_date: date, current_user_id: int) -> list[AvailabilityResponse]:
        rows = self.availability_repository.get_by_date(booking_date)
        availability: dict[int, AvailabilityResponse] = {}

        for room, slot, booking_user_id in rows:
            if room.id not in availability:
                availability[room.id] = AvailabilityResponse(
                    room_id=room.id,
                    room_name=room.name,
                    slots=[],
                )

            availability[room.id].slots.append(
                TimeSlotAvailability(
                    time_slot_id=slot.id,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    is_available=booking_user_id is None,
                    booked_by_me=booking_user_id == current_user_id,
                )
            )

        return list(availability.values())
