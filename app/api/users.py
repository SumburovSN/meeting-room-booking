from fastapi import APIRouter, Depends, status
from app.dependencies.current_user import get_current_user
from app.dependencies.roles import require_admin, require_owner_or_admin
from app.dependencies.services import get_user_service
from app.models.user import User
from app.schemas.user import UserResponse, EmployeeCreate, UserUpdate
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserResponse])
def get_all_users(
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_admin),
):
    return service.get_all()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: EmployeeCreate,
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_admin),
):
    return service.create_employee(email=data.email, password=data.password)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    user = service.get_by_id(user_id)
    require_owner_or_admin(current_user, user_id)
    return service.update_user(user, data.email, data.password)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    user = service.get_by_id(user_id)
    require_owner_or_admin(current_user, user_id)
    service.deactivate_user(user)
