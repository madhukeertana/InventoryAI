from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas import UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def current_user_profile(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return AuthService.to_out(current_user)
