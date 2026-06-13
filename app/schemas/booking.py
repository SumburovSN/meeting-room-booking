from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    room_id: int
    time_slot_id: int
    booking_date: date


class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    time_slot_id: int
    booking_date: date

    model_config = ConfigDict(from_attributes=True)