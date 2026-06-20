from datetime import date
from sqlalchemy.orm import Session
from app.models.booking import Booking


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, booking_id: int) -> Booking | None:
        return (
            self.db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

    def get_by_date(self, booking_date: date) -> list[Booking]:
        return (
            self.db.query(Booking)
            .filter(Booking.booking_date == booking_date)
            .all()
        )

    def get_all(self) -> list[Booking]:
        return (
            self.db.query(Booking)
            .all()
        )

    def get_by_user(self, user_id: int) -> list[Booking]:
        return (
            self.db.query(Booking)
            .filter(Booking.user_id == user_id)
            .all()
        )

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def delete(self, booking: Booking) -> None:
        self.db.delete(booking)
        self.db.commit()

    def get_by_slot_date(self, time_slot_id: int, booking_date: date) -> Booking | None:
        return (
            self.db.query(Booking)
            .filter(Booking.time_slot_id == time_slot_id)
            .filter(Booking.booking_date == booking_date)
            .first()
        )
