import csv
from datetime import datetime, timedelta, time
from app.core.database import SessionLocal
from app.models.room import Room
from app.models.time_slot import TimeSlot
from pathlib import Path
from app.core.config import settings


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


def get_or_create_room(db, room_name: str) -> Room:
    room = (
        db.query(Room)
        .filter(Room.name == room_name)
        .first()
    )
    if room:
        return room

    room = Room(name=room_name)

    db.add(room)
    db.commit()
    db.refresh(room)

    return room


def create_slots(db, room: Room, slots: list[tuple[time, time]]) -> None:
    for start_time, end_time in slots:
        exists = (
            db.query(TimeSlot)
            .filter(
                TimeSlot.room_id == room.id,
                TimeSlot.start_time == start_time,
                TimeSlot.end_time == end_time,
            )
            .first()
        )
        if exists:
            continue

        db.add(TimeSlot(room_id=room.id, start_time=start_time, end_time=end_time))
    db.commit()


def main():
    db = SessionLocal()
    csv_path = Path(settings.ROOMS_CSV_PATH)
    try:
        with open(csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                room = get_or_create_room(db, row["room_name"])
                slots = generate_slots(row["start_time"], row["end_time"], int(row["slot_minutes"]))
                create_slots(
                    db,
                    room,
                    slots,
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()
    # current_dir = Path.cwd()
    # print("Текущая директория:", current_dir)