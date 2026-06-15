from datetime import date
from fastapi import APIRouter, Depends, status
from app.dependencies.current_user import get_current_user
from app.dependencies.roles import require_admin
from app.dependencies.services import get_room_service, get_booking_service
from app.models.user import User
from app.schemas.room import (
    RoomCreate,
    RoomUpdate,
    RoomResponse,
)
from app.services.booking_service import BookingService
from app.services.room_service import RoomService


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    data: RoomCreate,
    service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    return service.create(data.name)


@router.get("/availability")
def get_availability(
    booking_date: date,
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_availability(booking_date)



@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(room_id)


@router.get("", response_model=list[RoomResponse])
def get_rooms(
    service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all()


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    data: RoomUpdate,
    service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    room = service.get_by_id(room_id)
    return service.update(room, data.name)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)
    room = service.get_by_id(room_id)
    service.delete(room)
