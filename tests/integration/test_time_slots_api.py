def test_create_time_slot_success(
    client,
    admin_auth_headers,
    db_session,
    room,
):
    response = client.post(
        "/time-slots",
        json={
            "room_id": room.id,
            "start_time": "09:00:00",
            "end_time": "10:00:00",
        },
        headers=admin_auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["room_id"] == room.id
    assert data["start_time"] == "09:00:00"
    assert data["end_time"] == "10:00:00"


def test_create_time_slot_overlap(
    client,
    admin_auth_headers,
    room,
    time_slot,
):
    response = client.post(
        "/time-slots",
        json={
            "room_id": room.id,
            "start_time": "09:30:00",
            "end_time": "10:30:00",
        },
        headers=admin_auth_headers,
    )

    assert response.status_code == 409


def test_get_room_slots(
    client,
    auth_headers,
    room,
    time_slot,
):
    response = client.get(
        f"/time-slots/room/{room.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == time_slot.id


def test_update_time_slot(
    client,
    admin_auth_headers,
    time_slot,
):
    response = client.put(
        f"/time-slots/{time_slot.id}",
        json={
            "start_time": "11:00:00",
            "end_time": "12:00:00",
        },
        headers=admin_auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["start_time"] == "11:00:00"
    assert data["end_time"] == "12:00:00"


def test_delete_time_slot(
    client,
    admin_auth_headers,
    db_session,
    time_slot,
):
    response = client.delete(
        f"/time-slots/{time_slot.id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204