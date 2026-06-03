from fastapi import HTTPException, status
from app.models.user import User, UserRole


def check_self_or_admin(
    current_user: User,
    target_user: User,
) -> None:

    if current_user.role == UserRole.admin:
        return

    if current_user.id == target_user.id:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied",
    )