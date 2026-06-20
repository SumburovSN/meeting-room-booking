from datetime import date
from fastapi import APIRouter, Depends
from app.dependencies.current_user import get_current_user
from app.dependencies.services import get_availability_service
from app.models import User
from app.schemas.availability import AvailabilityResponse
from app.services.availability_service import AvailabilityService


router = APIRouter(prefix="/availability", tags=["Availability"])


@router.get(
    "/{booking_date}",
    response_model=list[AvailabilityResponse],
    summary="Get room availability for a date",
    description="Returns all rooms with their time slots and booking status."
)
def get_available_slots(
    booking_date: date,
    service: AvailabilityService = Depends(get_availability_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_availability(booking_date, current_user.id)
