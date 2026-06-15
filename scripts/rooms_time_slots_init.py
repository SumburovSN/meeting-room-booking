import csv
from datetime import datetime, timedelta, time
from app.core.database import SessionLocal
from app.models.room import Room
from app.models.time_slot import TimeSlot
from pathlib import Path
from app.core.config import settings


class TimeSlotsRoomSeeding:
    def __init__(self) -> None:
        self.csv_path = Path(settings.ROOMS_CSV_PATH)
        self.db = SessionLocal()

    @staticmethod
    def generate_slots(start_time: str, end_time: str, slot_minutes: int)-> list[tuple[time, time]]:
        if slot_minutes <= 0:
            raise ValueError(
                "slot_minutes must be greater than zero"
            )
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        result = []
        current = start

        while current < end:
            next_time = current + timedelta(minutes=slot_minutes)
            if next_time > end:
                next_time = end

            result.append((current.time(), next_time.time()))
            current = next_time

        return result


    def get_or_create_room(self, room_name: str) -> Room:
        room = (
            self.db.query(Room)
            .filter(Room.name == room_name)
            .first()
        )
        if room:
            return room
        room = Room(name=room_name)

        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room


    def create_slots(self, room: Room, slots: list[tuple[time, time]]) -> None:
        for start_time, end_time in slots:
            exists = (
                self.db.query(TimeSlot)
                .filter(
                    TimeSlot.room_id == room.id,
                    TimeSlot.start_time == start_time,
                    TimeSlot.end_time == end_time,
                )
                .first()
            )
            if exists:
                continue

            self.db.add(TimeSlot(room_id=room.id, start_time=start_time, end_time=end_time))
        self.db.commit()

    def run(self):
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        try:
            with open(self.csv_path, newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    room = self.get_or_create_room(row["room_name"])
                    slots = self.generate_slots(row["start_time"], row["end_time"],int(row["slot_minutes"]))
                    self.create_slots(room, slots)
            print(f"Rooms initialized from {self.csv_path}")

        finally:
            self.db.close()


if __name__ == "__main__":
    TimeSlotsRoomSeeding().run()
