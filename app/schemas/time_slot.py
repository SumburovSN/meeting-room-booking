from datetime import time
from pydantic import BaseModel, ConfigDict


class TimeSlotCreate(BaseModel):
    room_id: int
    start_time: time
    end_time: time


class TimeSlotUpdate(BaseModel):
    start_time: time
    end_time: time


class TimeSlotResponse(BaseModel):
    id: int
    room_id: int
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)
