from datetime import date, datetime
from app.models.booking import Booking
from app.repositories.booking_repository import BookingRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.time_slot_repository import TimeSlotRepository
from app.repositories.user_repository import UserRepository
from app.services.exceptions import (
    BookingNotFoundError,
    SlotAlreadyBookedError,
    InvalidRoomTimeSlotError,
    UserNotFoundError,
    RoomNotFoundError,
    InvalidBookingDateError,
)


class BookingService:
    def __init__(self, booking_repository: BookingRepository, room_repository: RoomRepository,
                 time_slot_repository: TimeSlotRepository, user_repository: UserRepository):
        self.booking_repository = booking_repository
        self.room_repository = room_repository
        self.time_slot_repository = time_slot_repository
        self.user_repository = user_repository

    def get_by_id(self, booking_id: int) -> Booking:
        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundError()
        return booking

    def get_all(self) -> list[Booking]:
        return self.booking_repository.get_all()

    def get_by_user(self, user_id: int) -> list[Booking]:
        return self.booking_repository.get_by_user(user_id)

    def create_booking(self, user_id: int, room_id: int, time_slot_id: int, booking_date: date) -> Booking:
        user = self.user_repository.get_by_id(user_id)
        if user is None or not user.is_active:
            raise UserNotFoundError()

        if booking_date < date.today():
            raise InvalidBookingDateError()

        room = self.room_repository.get_by_id(room_id)
        if room is None:
            raise RoomNotFoundError()

        time_slot = self.time_slot_repository.get_by_id(time_slot_id)
        if time_slot is None:
            raise InvalidRoomTimeSlotError()
        if time_slot.room_id != room_id:
            raise InvalidRoomTimeSlotError()
        if booking_date == date.today():
            if time_slot.end_time <= datetime.now().time():
                raise InvalidBookingDateError()

        existing_booking = self.booking_repository.get_by_room_slot_date(room_id, time_slot_id, booking_date)
        if existing_booking is not None:
            raise SlotAlreadyBookedError()

        booking = Booking(user_id=user_id, room_id=room_id, time_slot_id=time_slot_id, booking_date=booking_date)
        return self.booking_repository.create(booking)

    def delete_booking(self, booking_id: int) -> None:
        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundError()

        self.booking_repository.delete(booking)
