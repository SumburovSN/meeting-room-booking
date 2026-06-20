from fastapi import Depends, HTTPException, status
from app.dependencies.current_user import get_current_user
from app.models.user import User, UserRole


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def require_owner_or_admin(current_user: User, owner_id: int) -> User:
    if current_user.role == UserRole.admin:
        return current_user
    if current_user.id == owner_id:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin or Owner access required",
    )
