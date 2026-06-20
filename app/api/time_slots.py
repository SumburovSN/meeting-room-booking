from fastapi import APIRouter, Depends, status
from app.dependencies.current_user import get_current_user
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.time_slot import (
    TimeSlotCreate,
    TimeSlotUpdate,
    TimeSlotResponse,
)
from app.services.time_slot_service import TimeSlotService
from app.dependencies.services import get_time_slot_service


router = APIRouter(
    prefix="/time-slots",
    tags=["Time Slots"],
)


@router.get("/room/{room_id}", response_model=list[TimeSlotResponse])
def get_room_slots(
    room_id: int,
    service: TimeSlotService = Depends(get_time_slot_service),
    _: User = Depends(get_current_user),
):
    return service.get_slots_by_room_id(room_id)


@router.post("", response_model=TimeSlotResponse, status_code=status.HTTP_201_CREATED)
def create_slot(
    data: TimeSlotCreate,
    service: TimeSlotService = Depends(get_time_slot_service),
    _: User = Depends(require_admin),
):
    return service.create_slot(room_id=data.room_id, start_time=data.start_time, end_time=data.end_time)


@router.put("/{slot_id}", response_model=TimeSlotResponse)
def update_slot(
    slot_id: int,
    data: TimeSlotUpdate,
    service: TimeSlotService = Depends(get_time_slot_service),
    _: User = Depends(require_admin),
):
    return service.update_slot(
        slot_id=slot_id,
        start_time=data.start_time,
        end_time=data.end_time,
    )


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(
    slot_id: int,
    service: TimeSlotService = Depends(get_time_slot_service),
    _: User = Depends(require_admin),
):
    service.delete_slot(slot_id)
