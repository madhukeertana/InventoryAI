from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas import ActionCardOut, ActionCardUpdate
from app.services.action_card_service import ActionCardService

router = APIRouter(prefix="/action-cards", tags=["action-cards"])


@router.get("/today", response_model=list[ActionCardOut])
def today_actions(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    regenerate: Annotated[bool, Query()] = True,
):
    return ActionCardService(db).today_cards(current_user, regenerate=regenerate)


@router.patch("/{card_id}", response_model=ActionCardOut)
def update_action_card(
    card_id: UUID,
    payload: ActionCardUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return ActionCardService(db).update_card(current_user, card_id, payload)
