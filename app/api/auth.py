from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.schemas.auth import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
# from app.schemas.auth import (
#     LoginRequest,
#     TokenResponse,
# )
from app.models.user import User
from app.core.security import (
    verify_password,
    create_access_token,
)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        user.id,
        user.role.value,
    )

    return TokenResponse(
        access_token=token,
    )