from sqlalchemy import Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    time_slot_id: Mapped[int] = mapped_column(ForeignKey("time_slots.id"), nullable=False)

    booking_date: Mapped[Date] = mapped_column(Date, nullable=False)

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    time_slot = relationship("TimeSlot", back_populates="bookings")

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "time_slot_id",
            "booking_date",
            name="uq_room_slot_date"
        ),
    )