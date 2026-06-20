from datetime import date
from sqlalchemy import and_, Row
from sqlalchemy.orm import Session
from app.models import Booking, Room, TimeSlot


class AvailabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_date(self, booking_date: date) -> list[Row]:
        return (
            self.db.query(
                Room,
                TimeSlot,
                Booking.user_id,
            )
            .join(Room.time_slots)
            .outerjoin(
                Booking,
                and_(
                    Booking.time_slot_id == TimeSlot.id,
                    Booking.booking_date == booking_date,
                ),
            )
            .order_by(Room.id, TimeSlot.start_time)
            .all()
        )
