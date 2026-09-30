from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.action_card import ActionCard
from app.models.ocr import InvoiceUpload


class ActionCardRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_day(
        self,
        organization_id: UUID,
        action_date: date,
        assignee_user_id: Optional[UUID] = None,
    ) -> list[ActionCard]:
        query = self.db.query(ActionCard).filter(
            ActionCard.organization_id == organization_id,
            ActionCard.action_date == action_date,
        )
        if assignee_user_id:
            query = query.filter(
                (ActionCard.assignee_user_id == assignee_user_id)
                | (ActionCard.assignee_user_id.is_(None))
            )
        return query.order_by(ActionCard.created_at.desc()).all()

    def get(self, card_id: UUID) -> Optional[ActionCard]:
        return self.db.get(ActionCard, card_id)

    def add_many(self, cards: list[ActionCard]) -> list[ActionCard]:
        self.db.add_all(cards)
        self.db.commit()
        for card in cards:
            self.db.refresh(card)
        return cards

    def save(self, card: ActionCard) -> ActionCard:
        self.db.commit()
        self.db.refresh(card)
        return card

    def delete_pending_for_day(self, organization_id: UUID, action_date: date) -> None:
        (
            self.db.query(ActionCard)
            .filter(
                ActionCard.organization_id == organization_id,
                ActionCard.action_date == action_date,
                ActionCard.status == "PENDING",
            )
            .delete(synchronize_session=False)
        )
        self.db.commit()


class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, upload: InvoiceUpload) -> InvoiceUpload:
        self.db.add(upload)
        self.db.commit()
        self.db.refresh(upload)
        return upload

    def get(self, upload_id: UUID) -> Optional[InvoiceUpload]:
        return self.db.get(InvoiceUpload, upload_id)
