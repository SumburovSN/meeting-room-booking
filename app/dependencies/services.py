from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.time_slot_service import TimeSlotService
from app.services.user_service import UserService
from app.repositories.room_repository import RoomRepository
from app.services.room_service import RoomService
from app.services.booking_service import BookingService
from app.repositories.booking_repository import BookingRepository
from app.repositories.time_slot_repository import TimeSlotRepository


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)


def get_room_service(db: Session = Depends(get_db)) -> RoomService:
    repository = RoomRepository(db)
    return RoomService(repository)


def get_booking_service(db: Session = Depends(get_db)) -> BookingService:
    return BookingService(
        booking_repository=BookingRepository(db),
        room_repository=RoomRepository(db),
        time_slot_repository=TimeSlotRepository(db),
        user_repository=UserRepository(db),
    )


def get_time_slot_service(db: Session = Depends(get_db)) -> TimeSlotService:
    return TimeSlotService(slot_repository=TimeSlotRepository(db), room_repository=RoomRepository(db))
