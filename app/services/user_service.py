from app.core.security import hash_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.services.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all(self) -> list[User]:
        return self.repository.get_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()
        return user

    def get_by_email(self, user_email: str) -> User:
        user = self.repository.get_by_email(email=user_email)

        if user is None:
            raise UserNotFoundError()
        return user

    def create_employee(self, email: str, password: str) -> User:
        if self.repository.get_by_email(email):
            raise UserAlreadyExistsError()
        user = User(
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.employee,
            is_active=True,
        )
        return self.repository.create(user)

    def update_user(self, user: User, email: str | None, password: str | None) -> User:
        if email is not None:
            existing_user = self.repository.get_by_email(email)
            if existing_user is not None and existing_user.id != user.id:
                raise UserAlreadyExistsError()
            user.email = email

        if password is not None:
            user.hashed_password = hash_password(password)

        return self.repository.update(user)

    def deactivate_user(
        self,
        user: User,
    ) -> User:

        user.is_active = False
        return self.repository.update(user)
    