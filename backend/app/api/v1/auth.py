from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.core.dependencies import Role, get_current_user, require_roles
from app.models.user import User
from app.schemas import LoginRequest, MessageOut, RegisterRequest, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite_normalized,
        domain=settings.cookie_domain or None,
        path=settings.cookie_path,
        max_age=settings.access_token_expire_minutes * 60,
    )


def _clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.cookie_name,
        path=settings.cookie_path,
        domain=settings.cookie_domain or None,
    )


@router.post("/login", response_model=UserOut)
def login(
    payload: LoginRequest,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
):
    user, token = AuthService(db).authenticate(payload.email, payload.password)
    _set_auth_cookie(response, token)
    return AuthService.to_out(user)


@router.post("/logout", response_model=MessageOut)
def logout(response: Response):
    _clear_auth_cookie(response)
    return MessageOut(message="Logged out")


@router.get("/me", response_model=UserOut)
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return AuthService.to_out(current_user)


@router.post("/register", response_model=UserOut)
def register(
    payload: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(Role.SYSTEM_ADMIN))],
):
    user = AuthService(db).register(payload, current_user)
    return AuthService.to_out(user)
