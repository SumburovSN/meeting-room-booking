from datetime import date, timedelta
from app.models.booking import Booking


def test_create_booking_success(
    client,
    employee_user,
    auth_headers,
    room,
    time_slot,
):
    response = client.post(
        "/bookings",
        json={
            "room_id": room.id,
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
    assert data["room_id"] == room.id
    assert data["time_slot_id"] == time_slot.id


def test_my_bookings(
    client,
    db_session,
    employee_user,
    auth_headers,
    room,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        room_id=room.id,
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
    room,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        room_id=room.id,
        time_slot_id=time_slot.id,
        booking_date=date.today() + timedelta(days=1),
    )

    db_session.add(booking)
    db_session.commit()

    response = client.post(
        "/bookings",
        json={
            "room_id": room.id,
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
    room,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        room_id=room.id,
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
    room,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        room_id=room.id,
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
    room,
    time_slot,
):
    booking = Booking(
        user_id=employee_user.id,
        room_id=room.id,
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
    room,
    time_slot,
):
    booking = Booking(
        user_id=employee_user_2.id,
        room_id=room.id,
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

# def test_get_my_bookings(client, db_session, auth_headers, room):
#     user = User(
#         email="employee@example.com",
#         hashed_password=hash_password("secret"),
#         role=UserRole.employee,
#         is_active=True,
#     )
#
#     room = Room(name="Conference Room")
#
#     db_session.add(user)
#     db_session.add(room)
#     db_session.commit()
#
#     slot = TimeSlot(
#         room_id=room.id,
#         start_time=time(10, 0),
#         end_time=time(11, 0),
#     )
#
#     db_session.add(slot)
#     db_session.commit()
#
#     booking = Booking(
#         user_id=user.id,
#         room_id=room.id,
#         time_slot_id=slot.id,
#         booking_date=date.today() + timedelta(days=1),
#     )
#
#     db_session.add(booking)
#     db_session.commit()
#
#     headers = create_auth_headers(user)
#
#     response = client.get(
#         "/bookings/my",
#         headers=headers,
#     )
#
#     assert response.status_code == 200
#
#     data = response.json()
#
#     assert len(data) == 1
#     assert data[0]["user_id"] == user.id
#
#
# def test_get_all_bookings_as_admin(client, db_session):
#     admin = User(
#         email="admin@example.com",
#         hashed_password=hash_password("secret"),
#         role=UserRole.admin,
#         is_active=True,
#     )
#
#     room = Room(name="Conference Room")
#
#     db_session.add(admin)
#     db_session.add(room)
#     db_session.commit()
#
#     slot = TimeSlot(
#         room_id=room.id,
#         start_time=time(10, 0),
#         end_time=time(11, 0),
#     )
#
#     db_session.add(slot)
#     db_session.commit()
#
#     booking = Booking(
#         user_id=admin.id,
#         room_id=room.id,
#         time_slot_id=slot.id,
#         booking_date=date.today() + timedelta(days=1),
#     )
#
#     db_session.add(booking)
#     db_session.commit()
#
#     headers = create_auth_headers(admin)
#
#     response = client.get(
#         "/bookings",
#         headers=headers,
#     )
#
#     assert response.status_code == 200
#
#     data = response.json()
#
#     assert len(data) == 1
#
#
# def test_delete_booking_success(client, db_session):
#     user = User(
#         email="employee@example.com",
#         hashed_password=hash_password("secret"),
#         role=UserRole.employee,
#         is_active=True,
#     )
#
#     room = Room(name="Conference Room")
#
#     db_session.add(user)
#     db_session.add(room)
#     db_session.commit()
#
#     slot = TimeSlot(
#         room_id=room.id,
#         start_time=time(10, 0),
#         end_time=time(11, 0),
#     )
#
#     db_session.add(slot)
#     db_session.commit()
#
#     booking = Booking(
#         user_id=user.id,
#         room_id=room.id,
#         time_slot_id=slot.id,
#         booking_date=date.today() + timedelta(days=1),
#     )
#
#     db_session.add(booking)
#     db_session.commit()
#
#     headers = create_auth_headers(user)
#
#     response = client.delete(
#         f"/bookings/{booking.id}",
#         headers=headers,
#     )
#
#     assert response.status_code == 204
#
#     deleted = (
#         db_session.query(Booking)
#         .filter(Booking.id == booking.id)
#         .first()
#     )
#
#     assert deleted is None
