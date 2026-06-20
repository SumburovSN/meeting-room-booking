from datetime import date, timedelta
from app.models.booking import Booking


def test_create_booking_success(
    client,
    employee_user,
    auth_headers,
    time_slot,
):
    response = client.post(
        "/bookings",
        json={
            "time_slot_id": time_slot.id,
            "booking_date": str(
                date.today() + timedelta(days=1)
            ),
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] == employee_user.id
    assert data["time_slot_id"] == time_slot.id


def test_my_bookings(
    client,
    db_session,
    employee_user,
    auth_headers,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        time_slot_id=time_slot.id,
        booking_date=date.today() + timedelta(days=1),
    )

    db_session.add(booking)
    db_session.commit()

    response = client.get(
        "/bookings/my",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == booking.id


def test_create_booking_slot_already_booked(
    client,
    db_session,
    employee_user,
    auth_headers,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        time_slot_id=time_slot.id,
        booking_date=date.today() + timedelta(days=1),
    )

    db_session.add(booking)
    db_session.commit()

    response = client.post(
        "/bookings",
        json={
            "time_slot_id": time_slot.id,
            "booking_date": str(
                date.today() + timedelta(days=1)
            ),
        },
        headers=auth_headers,
    )

    assert response.status_code == 409


def test_get_all_bookings(
    client,
    db_session,
    employee_user,
    admin_auth_headers,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        time_slot_id=time_slot.id,
        booking_date=date.today() + timedelta(days=1),
    )

    db_session.add(booking)
    db_session.commit()

    response = client.get(
        "/bookings",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1


def test_get_all_bookings_forbidden(
    client,
    auth_headers,
):
    response = client.get(
        "/bookings",
        headers=auth_headers,
    )

    assert response.status_code == 403


def test_delete_own_booking(
    client,
    db_session,
    employee_user,
    auth_headers,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        time_slot_id=time_slot.id,
        booking_date=date.today() + timedelta(days=1),
    )

    db_session.add(booking)
    db_session.commit()

    response = client.delete(
        f"/bookings/{booking.id}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_admin_can_delete_booking(
    client,
    db_session,
    employee_user,
    admin_auth_headers,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        time_slot_id=time_slot.id,
        booking_date=date.today() + timedelta(days=1),
    )

    db_session.add(booking)
    db_session.commit()

    response = client.delete(
        f"/bookings/{booking.id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204


def test_delete_other_user_booking_forbidden(
    client,
    db_session,
    employee_user,
    employee_user_2,
    auth_headers,
    time_slot,
):
    booking = Booking(
        user_id=employee_user_2.id,
        time_slot_id=time_slot.id,
        booking_date=date.today() + timedelta(days=1),
    )

    db_session.add(booking)
    db_session.commit()

    response = client.delete(
        f"/bookings/{booking.id}",
        headers=auth_headers,
    )

    assert response.status_code == 403
