from fastapi import APIRouter, Depends, status
from app.dependencies.roles import require_admin
from app.dependencies.services import get_booking_service
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import BookingService
from app.dependencies.current_user import get_current_user
from app.services.permissions import check_booking_owner_or_admin


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("",response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    data: BookingCreate,
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_booking(
        user_id=current_user.id,
        room_id=data.room_id,
        time_slot_id=data.time_slot_id,
        booking_date=data.booking_date,
    )


@router.get("/my", response_model=list[BookingResponse])
def my_bookings(
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_user(current_user.id)


@router.get("",response_model=list[BookingResponse])
def get_all_bookings(
    service: BookingService = Depends(get_booking_service),
    _: User = Depends(require_admin),
):
    return service.get_all()


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    booking = service.get_by_id(booking_id)
    check_booking_owner_or_admin(current_user, booking)
    service.delete_booking(booking_id)

