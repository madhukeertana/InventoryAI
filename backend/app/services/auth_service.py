from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import Role
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas import RegisterRequest, UserOut


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def authenticate(self, email: str, password: str) -> tuple[User, str]:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )
        token = create_access_token(
            user_id=user.id,
            role=user.role,
            organization_id=user.organization_id,
            location_id=user.location_id,
        )
        return user, token

    def register(self, payload: RegisterRequest, actor: User) -> User:
        if actor.role != Role.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only system admin can register users",
            )
        if self.repo.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        try:
            if payload.role not in Role.values():
                raise ValueError("invalid role")
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role",
            ) from exc

        user = User(
            email=payload.email.lower(),
            password_hash=hash_password(payload.password),
            full_name=payload.full_name,
            role=payload.role,
            organization_id=payload.organization_id,
            location_id=payload.location_id,
            is_active=True,
        )
        return self.repo.create(user)

    @staticmethod
    def to_out(user: User) -> UserOut:
        return UserOut.model_validate(user)
