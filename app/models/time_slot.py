from sqlalchemy import Integer, Time, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time
from app.core.database import Base


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    room = relationship("Room", back_populates="time_slots")
    bookings = relationship("Booking", back_populates="time_slot")

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "start_time",
            "end_time",
            name="uq_room_time_slot",
        ),
    )
