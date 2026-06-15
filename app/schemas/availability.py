from datetime import time
from pydantic import BaseModel


class SlotAvailabilityResponse(BaseModel):
    room_id: int
    room_name: str

    time_slot_id: int
    start_time: time
    end_time: time

    is_available: bool
