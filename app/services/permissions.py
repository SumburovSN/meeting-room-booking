from app.models.user import User, UserRole
from app.services.exceptions import ForbiddenOperationError
from app.models.booking import Booking


def check_self_or_admin(current_user: User, target_user: User) -> None:
    if current_user.role == UserRole.admin:
        return
    if current_user.id == target_user.id:
        return
    raise ForbiddenOperationError()


def check_booking_owner_or_admin(current_user: User, booking: Booking):
    if current_user.role == UserRole.admin:
        return
    if booking.user_id == current_user.id:
        return
    raise ForbiddenOperationError()