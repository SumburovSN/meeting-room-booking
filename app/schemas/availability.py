from datetime import time
from pydantic import BaseModel, ConfigDict


class TimeSlotAvailability(BaseModel):
    time_slot_id: int
    start_time: time
    end_time: time
    is_available: bool
    booked_by_me: bool

    model_config = ConfigDict(from_attributes=True)


class AvailabilityResponse(BaseModel):
    room_id: int
    room_name: str
    slots: list[TimeSlotAvailability]

    model_config = ConfigDict(from_attributes=True)
