from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole


ADMIN_EMAIL = "admin@bookroom.local"
ADMIN_PASSWORD = "admin123"


def main():
    db: Session = SessionLocal()

    try:
        existing_admin = (
            db.query(User)
            .filter(User.email == ADMIN_EMAIL)
            .first()
        )

        if existing_admin:
            print("Admin already exists")
            return

        admin = User(
            email=ADMIN_EMAIL,
            hashed_password=hash_password(ADMIN_PASSWORD),
            role=UserRole.admin,
        )

        db.add(admin)
        db.commit()

        print("Admin created successfully")
        print(f"Email: {ADMIN_EMAIL}")
        print(f"Password: {ADMIN_PASSWORD}")

    finally:
        db.close()


if __name__ == "__main__":
    main()