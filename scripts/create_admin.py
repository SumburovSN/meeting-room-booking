# bash: ADMIN_EMAIL=superadmin@bookroom.com ADMIN_PASSWORD=secret poetry run python -m scripts.create_admin

from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.schemas.user import EmployeeCreate
from app.core.config import settings


class AdminCreator:
    def __init__(self):
        self.db: Session = SessionLocal()

    @staticmethod
    def get_admin_env() -> EmployeeCreate | None:
        admin_email = settings.ADMIN_EMAIL
        admin_password = settings.ADMIN_PASSWORD

        if not admin_email or not admin_password:
            raise RuntimeError("ADMIN_EMAIL / ADMIN_PASSWORD not set")
        try:
            return EmployeeCreate(email=admin_email, password=admin_password)
        except ValidationError as e:
            print(e)

    @staticmethod
    def input_handling() -> EmployeeCreate | None:
        while True:
            print("New Admin adding (N/n for exit)")
            email = input("Input admin email: ").strip()
            if email.lower() == "n":
                return None
            password = input("Input admin password: ")
            try:
                return EmployeeCreate(email=email, password=password)
            except ValidationError as e:
                print(e)

    def add_admin(self, user: EmployeeCreate):
        existing_admin = (
            self.db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_admin:
            print(f"Admin with email {user.email} already exists")
            return

        admin = User(
            email=user.email,
            hashed_password=hash_password(user.password),
            role=UserRole.admin,
        )

        self.db.add(admin)
        self.db.commit()

        print("Admin created successfully")
        print(f"Email: {user.email}")

    def run_input(self):
        try:
            user = self.input_handling()
            if user:
                self.add_admin(user)
        finally:
            self.db.close()

    def run(self):
        try:
            user = self.get_admin_env()
            if user:
                self.add_admin(user)
        finally:
            self.db.close()


if __name__ == "__main__":
    AdminCreator().run()
