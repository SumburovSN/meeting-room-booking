from unittest.mock import Mock, patch
import pytest
from app.services.auth_service import AuthService
from app.services.exceptions import InvalidCredentialsError


@pytest.fixture
def repository():
    return Mock()


@pytest.fixture
def service(repository):
    return AuthService(repository)


@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.verify_password")
def test_authorize_success(
    verify_password_mock,
    create_access_token_mock,
    service,
    repository,
):
    user = Mock()
    user.id = 1
    user.role.value = "admin"
    user.is_active = True
    user.hashed_password = "hashed-password"

    repository.get_by_email.return_value = user

    verify_password_mock.return_value = True
    create_access_token_mock.return_value = "jwt-token"

    result = service.authorize(
        "admin@test.com",
        "password123",
    )

    assert result == "jwt-token"

    repository.get_by_email.assert_called_once_with(
        "admin@test.com"
    )

    verify_password_mock.assert_called_once_with(
        "password123",
        "hashed-password",
    )

    create_access_token_mock.assert_called_once_with(
        1,
        "admin",
    )


def test_authorize_user_not_found(
    service,
    repository,
):
    repository.get_by_email.return_value = None

    with pytest.raises(InvalidCredentialsError):
        service.authorize(
            "missing@test.com",
            "password123",
        )

    repository.get_by_email.assert_called_once_with(
        "missing@test.com"
    )


def test_authorize_inactive_user(
    service,
    repository,
):
    user = Mock()
    user.is_active = False

    repository.get_by_email.return_value = user

    with pytest.raises(InvalidCredentialsError):
        service.authorize(
            "admin@test.com",
            "password123",
        )


@patch("app.services.auth_service.verify_password")
def test_authorize_invalid_password(
    verify_password_mock,
    service,
    repository,
):
    user = Mock()
    user.is_active = True
    user.hashed_password = "hashed-password"

    repository.get_by_email.return_value = user

    verify_password_mock.return_value = False

    with pytest.raises(InvalidCredentialsError):
        service.authorize(
            "admin@test.com",
            "wrong-password",
        )

    verify_password_mock.assert_called_once_with(
        "wrong-password",
        "hashed-password",
    )