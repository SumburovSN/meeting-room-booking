from datetime import date, timedelta
from app.models import Booking


def test_get_availability_no_bookings(
    client,
    auth_headers,
    room,
    time_slot,
):
    booking_date = date.today() + timedelta(days=1)

    response = client.get(
        f"/availability/{booking_date}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["room_id"] == room.id
    assert data[0]["room_name"] == room.name

    assert len(data[0]["slots"]) == 1

    slot = data[0]["slots"][0]

    assert slot["time_slot_id"] == time_slot.id
    assert slot["is_available"] is True
    assert slot["booked_by_me"] is False


def test_get_availability_booked_by_me(
    client,
    db_session,
    auth_headers,
    employee_user,
    room,
    time_slot,
):
    booking_date = date.today() + timedelta(days=1)

    booking = Booking(
        user_id=employee_user.id,
        time_slot_id=time_slot.id,
        booking_date=booking_date,
    )

    db_session.add(booking)
    db_session.commit()

    response = client.get(
        f"/availability/{booking_date}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    slot = data[0]["slots"][0]

    assert slot["time_slot_id"] == time_slot.id
    assert slot["is_available"] is False
    assert slot["booked_by_me"] is True
