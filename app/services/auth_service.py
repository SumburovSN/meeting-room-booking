from app.core.security import verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.services.exceptions import InvalidCredentialsError


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authorize(self, email: str, password: str) -> str:
        user = self.repository.get_by_email(email)

        if not user:
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        return create_access_token(user.id, user.role.value)
