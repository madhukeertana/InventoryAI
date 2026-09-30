from typing import Annotated, Callable
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

settings = get_settings()


class Role:
    PHARMACY_OWNER = "PHARMACY_OWNER"
    STORE_MANAGER = "STORE_MANAGER"
    PROCUREMENT_MANAGER = "PROCUREMENT_MANAGER"
    HOSPITAL_INCHARGE = "HOSPITAL_INCHARGE"
    WAREHOUSE_BRANCH_MANAGER = "WAREHOUSE_BRANCH_MANAGER"
    MULTI_OUTLET_INVENTORY_HEAD = "MULTI_OUTLET_INVENTORY_HEAD"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"

    @classmethod
    def values(cls) -> set[str]:
        return {
            cls.PHARMACY_OWNER,
            cls.STORE_MANAGER,
            cls.PROCUREMENT_MANAGER,
            cls.HOSPITAL_INCHARGE,
            cls.WAREHOUSE_BRANCH_MANAGER,
            cls.MULTI_OUTLET_INVENTORY_HEAD,
            cls.SYSTEM_ADMIN,
        }


def get_current_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    token = request.cookies.get(settings.cookie_name)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = decode_access_token(token)
        user_id = UUID(payload["sub"])
    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )

    user = UserRepository(db).get_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User inactive or not found",
        )
    return user


def require_roles(*roles: str) -> Callable:
    allowed = set(roles)

    def _dependency(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed and current_user.role != Role.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _dependency
