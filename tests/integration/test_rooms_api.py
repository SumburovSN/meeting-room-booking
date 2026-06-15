from app.models.user import User, UserRole
from app.models.room import Room
from app.core.security import hash_password


def create_admin(db_session):
    admin = User(
        email="admin@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


def create_employee(db_session):
    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    return employee


def get_token(client, email, password):
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    return response.json()["access_token"]


def test_create_room_as_admin(client, db_session):
    create_admin(db_session)

    token = get_token(
        client,
        "admin@example.com",
        "secret",
    )

    response = client.post(
        "/rooms",
        json={
            "name": "Conference Room",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Conference Room"
    assert "id" in body


def test_get_room_by_id(client, db_session):
    create_admin(db_session)

    room = Room(name="Meeting Room")
    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    token = get_token(
        client,
        "admin@example.com",
        "secret",
    )

    response = client.get(
        f"/rooms/{room.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == room.id
    assert body["name"] == "Meeting Room"


def test_get_all_rooms(client, db_session):
    create_admin(db_session)

    db_session.add(Room(name="Room A"))
    db_session.add(Room(name="Room B"))
    db_session.commit()

    token = get_token(
        client,
        "admin@example.com",
        "secret",
    )

    response = client.get(
        "/rooms",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    rooms = response.json()

    assert len(rooms) >= 2


def test_create_room_forbidden_for_employee(client, db_session):
    create_employee(db_session)

    token = get_token(
        client,
        "employee@example.com",
        "secret",
    )

    response = client.post(
        "/rooms",
        json={
            "name": "Secret Room",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403


def test_update_room_as_admin(client, db_session):
    create_admin(db_session)

    room = Room(name="Old Room")
    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    token = get_token(
        client,
        "admin@example.com",
        "secret",
    )

    response = client.put(
        f"/rooms/{room.id}",
        json={
            "name": "New Room",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    db_session.refresh(room)

    assert room.name == "New Room"


def test_update_room_forbidden_for_employee(client, db_session):
    create_employee(db_session)

    room = Room(name="Room A")
    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    token = get_token(
        client,
        "employee@example.com",
        "secret",
    )

    response = client.put(
        f"/rooms/{room.id}",
        json={
            "name": "Hacked Room",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403


def test_delete_room_as_admin(client, db_session):
    create_admin(db_session)

    room = Room(name="Room To Delete")
    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    token = get_token(
        client,
        "admin@example.com",
        "secret",
    )

    response = client.delete(
        f"/rooms/{room.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 204

    deleted_room = (
        db_session.query(Room)
        .filter(Room.id == room.id)
        .first()
    )

    assert deleted_room is None


def test_delete_room_forbidden_for_employee(client, db_session):
    create_employee(db_session)

    room = Room(name="Room A")
    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    token = get_token(
        client,
        "employee@example.com",
        "secret",
    )

    response = client.delete(
        f"/rooms/{room.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403


def test_get_room_not_found(client, db_session):
    create_admin(db_session)

    token = get_token(
        client,
        "admin@example.com",
        "secret",
    )

    response = client.get(
        "/rooms/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404


def test_create_duplicate_room(client, db_session):
    create_admin(db_session)

    room = Room(name="Conference Room")
    db_session.add(room)
    db_session.commit()

    token = get_token(
        client,
        "admin@example.com",
        "secret",
    )

    response = client.post(
        "/rooms",
        json={
            "name": "Conference Room",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 409
