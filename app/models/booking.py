from sqlalchemy import Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.core.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    time_slot_id: Mapped[int] = mapped_column(ForeignKey("time_slots.id", ondelete="CASCADE"), nullable=False)
    booking_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    user = relationship("User", back_populates="bookings")
    time_slot = relationship("TimeSlot", back_populates="bookings")

    __table_args__ = (
        UniqueConstraint(
            "time_slot_id",
            "booking_date",
            name="uq_time_slot_date",
        ),
    )
