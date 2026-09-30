from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import Role
from app.models.action_card import ActionCard
from app.models.user import User
from app.repositories.action_card_repository import ActionCardRepository
from app.repositories.inventory_repository import InventoryRepository
from app.rules.inventory_rules import (
    days_until_expiry,
    is_near_expiry,
    needs_cold_chain_alert,
    suggested_reorder_qty,
)
from app.schemas import ActionCardOut, ActionCardUpdate
from app.services.demand_service import DemandService
from app.services.license_service import LicenseService


class ActionCardService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ActionCardRepository(db)
        self.inventory_repo = InventoryRepository(db)
        self.demand = DemandService()
        self.license = LicenseService()

    def today_cards(self, user: User, regenerate: bool = True) -> list[ActionCardOut]:
        if not user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has no organization",
            )
        today = date.today()
        if regenerate:
            self._regenerate(user, today)
        cards = self.repo.list_for_day(user.organization_id, today)
        return [ActionCardOut.model_validate(c) for c in cards]

    def update_card(
        self, user: User, card_id, payload: ActionCardUpdate
    ) -> ActionCardOut:
        card = self.repo.get(card_id)
        if not card or card.organization_id != user.organization_id:
            if user.role != Role.SYSTEM_ADMIN:
                raise HTTPException(status_code=404, detail="Action card not found")
            if not card:
                raise HTTPException(status_code=404, detail="Action card not found")
        card.status = payload.status
        return ActionCardOut.model_validate(self.repo.save(card))

    def _regenerate(self, user: User, today: date) -> None:
        org_id = user.organization_id
        assert org_id is not None
        self.repo.delete_pending_for_day(org_id, today)
        batches = self.inventory_repo.list_batches(org_id)
        cards: list[ActionCard] = []

        for batch in batches:
            medicine = batch.medicine
            if not medicine:
                continue
            cover = self.demand.estimate_days_of_cover(batch.quantity, batch.velocity_tag)

            if is_near_expiry(batch.expiry_date, today=today):
                days = days_until_expiry(batch.expiry_date, today)
                cards.append(
                    ActionCard(
                        organization_id=org_id,
                        assignee_user_id=user.id,
                        card_type="SELL_FIRST",
                        status="PENDING",
                        reason=f"{medicine.name} batch {batch.batch_no} expires in {days} days — FEFO sell-first",
                        payload={
                            "batch_id": str(batch.id),
                            "medicine": medicine.name,
                            "expiry_date": batch.expiry_date.isoformat(),
                        },
                        action_date=today,
                    )
                )
                if days <= 30:
                    cards.append(
                        ActionCard(
                            organization_id=org_id,
                            assignee_user_id=user.id,
                            card_type="RETURN",
                            status="PENDING",
                            reason=f"Consider supplier return for {medicine.name} ({batch.batch_no}) within return window",
                            payload={"batch_id": str(batch.id)},
                            action_date=today,
                        )
                    )

            if cover is not None and cover <= 10:
                qty = suggested_reorder_qty(batch.quantity, batch.velocity_tag)
                cards.append(
                    ActionCard(
                        organization_id=org_id,
                        assignee_user_id=user.id,
                        card_type="ORDER",
                        status="PENDING",
                        reason=f"{medicine.name} may stock out in ~{cover} days. Suggest order {qty} units.",
                        payload={
                            "medicine_id": str(medicine.id),
                            "suggested_qty": qty,
                            "days_of_cover": cover,
                        },
                        action_date=today,
                    )
                )

            if needs_cold_chain_alert(batch.cold_chain_flag, medicine.requires_cold_chain):
                cards.append(
                    ActionCard(
                        organization_id=org_id,
                        assignee_user_id=user.id,
                        card_type="TRANSFER",
                        status="PENDING",
                        reason=f"Cold-chain item {medicine.name} tagged 2-8°C — verify fridge placement / transfer if surplus",
                        payload={
                            "batch_id": str(batch.id),
                            "storage": "2-8C",
                        },
                        action_date=today,
                    )
                )

        license_alert = self.license.check_org_license(self.db, org_id)
        if license_alert:
            cards.append(
                ActionCard(
                    organization_id=org_id,
                    assignee_user_id=user.id,
                    card_type="LICENSE_ALERT",
                    status="PENDING",
                    reason=license_alert["reason"],
                    payload=license_alert,
                    action_date=today,
                )
            )

        # Deduplicate by type+reason for MVP cleanliness
        unique: dict[str, ActionCard] = {}
        for card in cards:
            key = f"{card.card_type}:{card.reason}"
            unique[key] = card
        self.repo.add_many(list(unique.values())[:25])
