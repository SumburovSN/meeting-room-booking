from fastapi import APIRouter, Depends
from app.schemas.auth import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import AuthService
from app.dependencies.services import get_auth_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    return TokenResponse(access_token=service.authorize(form_data.username, form_data.password))
