from unittest.mock import Mock, patch
import pytest
from app.models.user import User, UserRole
from app.services.user_service import UserService
from app.services.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)


@pytest.fixture
def repository():
    return Mock()


@pytest.fixture
def service(repository):
    return UserService(repository)


def test_get_all_returns_users(
    service,
    repository,
):
    users = [Mock(), Mock()]

    repository.get_all.return_value = users

    result = service.get_all()

    assert result == users
    repository.get_all.assert_called_once()


def test_get_by_id_success(
    service,
    repository,
):
    user = Mock()

    repository.get_by_id.return_value = user

    result = service.get_by_id(1)

    assert result == user
    repository.get_by_id.assert_called_once_with(1)


def test_get_by_id_not_found(
    service,
    repository,
):
    repository.get_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        service.get_by_id(1)


def test_get_by_email_success(
    service,
    repository,
):
    user = Mock()

    repository.get_by_email.return_value = user

    result = service.get_by_email("user@test.com")

    assert result == user
    repository.get_by_email.assert_called_once_with(
        email="user@test.com"
    )


def test_get_by_email_not_found(
    service,
    repository,
):
    repository.get_by_email.return_value = None

    with pytest.raises(UserNotFoundError):
        service.get_by_email("user@test.com")


@patch("app.services.user_service.hash_password")
def test_create_employee_success(
    hash_password_mock,
    service,
    repository,
):
    hash_password_mock.return_value = "hashed-password"

    created_user = Mock()

    repository.get_by_email.return_value = None
    repository.create.return_value = created_user

    result = service.create_employee(
        "user@test.com",
        "password123",
    )

    assert result == created_user

    repository.get_by_email.assert_called_once_with(
        "user@test.com"
    )

    hash_password_mock.assert_called_once_with(
        "password123"
    )

    repository.create.assert_called_once()


def test_create_employee_user_already_exists(
    service,
    repository,
):
    repository.get_by_email.return_value = Mock()

    with pytest.raises(UserAlreadyExistsError):
        service.create_employee(
            "user@test.com",
            "password123",
        )


def test_update_user_email_success(
    service,
    repository,
):
    user = User(
        id=1,
        email="old@test.com",
        hashed_password="hash",
        role=UserRole.employee,
        is_active=True,
    )

    repository.get_by_email.return_value = None
    repository.update.return_value = user

    result = service.update_user(
        user=user,
        email="new@test.com",
        password=None,
    )

    assert result == user
    assert user.email == "new@test.com"

    repository.update.assert_called_once_with(user)


def test_update_user_duplicate_email(
    service,
    repository,
):
    user = User(
        id=1,
        email="old@test.com",
        hashed_password="hash",
        role=UserRole.employee,
        is_active=True,
    )

    existing_user = User(
        id=2,
        email="new@test.com",
        hashed_password="hash",
        role=UserRole.employee,
        is_active=True,
    )

    repository.get_by_email.return_value = existing_user

    with pytest.raises(UserAlreadyExistsError):
        service.update_user(
            user=user,
            email="new@test.com",
            password=None,
        )


@patch("app.services.user_service.hash_password")
def test_update_user_password_success(
    hash_password_mock,
    service,
    repository,
):
    user = User(
        id=1,
        email="user@test.com",
        hashed_password="old-hash",
        role=UserRole.employee,
        is_active=True,
    )

    hash_password_mock.return_value = "new-hash"
    repository.update.return_value = user

    result = service.update_user(
        user=user,
        email=None,
        password="new-password",
    )

    assert result == user
    assert user.hashed_password == "new-hash"

    hash_password_mock.assert_called_once_with(
        "new-password"
    )


def test_deactivate_user(
    service,
    repository,
):
    user = User(
        id=1,
        email="user@test.com",
        hashed_password="hash",
        role=UserRole.employee,
        is_active=True,
    )

    repository.update.return_value = user

    result = service.deactivate_user(user)

    assert result == user
    assert user.is_active is False

    repository.update.assert_called_once_with(user)
