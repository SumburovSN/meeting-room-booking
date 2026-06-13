from app.models.user import User, UserRole
from app.core.security import hash_password


def test_login_success(client, db_session):
    user = User(
        email="admin@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_password(client, db_session):
    user = User(
        email="admin@example.com",
        hashed_password=hash_password("secret"),
        role=UserRole.admin,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
