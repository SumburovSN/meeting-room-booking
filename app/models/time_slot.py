from sqlalchemy import Integer, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)

    start_time: Mapped[str] = mapped_column(Time, nullable=False)
    end_time: Mapped[str] = mapped_column(Time, nullable=False)

    room = relationship("Room", back_populates="time_slots")
    bookings = relationship("Booking", back_populates="time_slot")