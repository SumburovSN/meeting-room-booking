from app.core.security import hash_password
from app.models.user import User, UserRole


def test_get_all_users_as_admin(client, db_session):
    admin = User(
        email="admin@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )

    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add(admin)
    db_session.add(employee)
    db_session.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "secret",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    emails = {user["email"] for user in body}

    assert "admin@example.com" in emails
    assert "employee@example.com" in emails


def test_get_all_users_forbidden_for_employee(client, db_session):
    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add(employee)
    db_session.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "employee@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_register_employee_as_admin(client, db_session):
    admin = User(
        email="admin@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )

    db_session.add(admin)
    db_session.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/users/register",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": "employee@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    created_user = (
        db_session.query(User)
        .filter(User.email == "employee@example.com")
        .first()
    )

    assert created_user is not None
    assert created_user.role == UserRole.employee
    assert created_user.is_active is True


def test_register_employee_forbidden_for_employee(client, db_session):
    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add(employee)
    db_session.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "employee@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/users/register",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": "new@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 403


def test_update_own_profile(client, db_session):
    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "employee@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.put(
        f"/users/{employee.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": "updated@example.com",
            "password": None,
        },
    )

    assert response.status_code == 200

    db_session.refresh(employee)

    assert employee.email == "updated@example.com"


def test_update_other_user_forbidden(client, db_session):
    user1 = User(
        email="user1@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    user2 = User(
        email="user2@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add_all([user1, user2])
    db_session.commit()
    db_session.refresh(user2)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "user1@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.put(
        f"/users/{user2.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": "hacked@example.com",
            "password": None,
        },
    )

    assert response.status_code == 403


def test_admin_can_update_any_user(client, db_session):
    admin = User(
        email="admin@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )

    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add_all([admin, employee])
    db_session.commit()
    db_session.refresh(employee)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.put(
        f"/users/{employee.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "email": "updated@example.com",
            "password": None,
        },
    )

    assert response.status_code == 200

    db_session.refresh(employee)

    assert employee.email == "updated@example.com"


def test_deactivate_self(client, db_session):
    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "employee@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/users/{employee.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    db_session.refresh(employee)

    assert employee.is_active is False


def test_deactivate_other_user_forbidden(client, db_session):
    user1 = User(
        email="user1@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    user2 = User(
        email="user2@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add_all([user1, user2])
    db_session.commit()
    db_session.refresh(user2)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "user1@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/users/{user2.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_admin_can_deactivate_any_user(client, db_session):
    admin = User(
        email="admin@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )

    employee = User(
        email="employee@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.employee,
        is_active=True,
    )

    db_session.add_all([admin, employee])
    db_session.commit()
    db_session.refresh(employee)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "secret",
        },
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/users/{employee.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    db_session.refresh(employee)

    assert employee.is_active is False


