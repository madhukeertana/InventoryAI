from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import Role
from app.models.inventory import Medicine, StockBatch
from app.models.user import User
from app.repositories.inventory_repository import InventoryRepository
from app.rules.inventory_rules import classify_velocity
from app.schemas import (
    BatchCreate,
    BatchOut,
    BatchUpdate,
    MedicineCreate,
    MedicineOut,
    MedicineUpdate,
)


class InventoryService:
    def __init__(self, db: Session):
        self.repo = InventoryRepository(db)

    def _org_id(self, user: User) -> UUID:
        if user.role == Role.SYSTEM_ADMIN:
            if not user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Admin must be assigned an organization for inventory ops",
                )
        if not user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has no organization",
            )
        return user.organization_id

    def list_medicines(self, user: User) -> list[MedicineOut]:
        org_id = self._org_id(user)
        return [MedicineOut.model_validate(m) for m in self.repo.list_medicines(org_id)]

    def create_medicine(self, user: User, payload: MedicineCreate) -> MedicineOut:
        org_id = self._org_id(user)
        medicine = Medicine(
            organization_id=org_id,
            name=payload.name,
            sku=payload.sku,
            requires_cold_chain=payload.requires_cold_chain,
        )
        return MedicineOut.model_validate(self.repo.create_medicine(medicine))

    def update_medicine(
        self, user: User, medicine_id: UUID, payload: MedicineUpdate
    ) -> MedicineOut:
        medicine = self._get_org_medicine(user, medicine_id)
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(medicine, key, value)
        return MedicineOut.model_validate(self.repo.update_medicine(medicine))

    def delete_medicine(self, user: User, medicine_id: UUID) -> None:
        medicine = self._get_org_medicine(user, medicine_id)
        self.repo.delete_medicine(medicine)

    def list_batches(self, user: User) -> list[BatchOut]:
        org_id = self._org_id(user)
        location_id = user.location_id
        if user.role in {
            Role.MULTI_OUTLET_INVENTORY_HEAD,
            Role.HOSPITAL_INCHARGE,
            Role.WAREHOUSE_BRANCH_MANAGER,
            Role.PROCUREMENT_MANAGER,
            Role.SYSTEM_ADMIN,
        }:
            location_id = None
        batches = self.repo.list_batches(org_id, location_id)
        return [self._batch_out(b) for b in batches]

    def create_batch(self, user: User, payload: BatchCreate) -> BatchOut:
        medicine = self._get_org_medicine(user, payload.medicine_id)
        velocity = payload.velocity_tag or classify_velocity(payload.quantity)
        cold = payload.cold_chain_flag or medicine.requires_cold_chain
        batch = StockBatch(
            medicine_id=payload.medicine_id,
            location_id=payload.location_id,
            batch_no=payload.batch_no,
            expiry_date=payload.expiry_date,
            quantity=payload.quantity,
            cold_chain_flag=cold,
            velocity_tag=velocity,
        )
        created = self.repo.create_batch(batch)
        loaded = self.repo.get_batch(created.id)
        return self._batch_out(loaded or created)

    def update_batch(
        self, user: User, batch_id: UUID, payload: BatchUpdate
    ) -> BatchOut:
        batch = self._get_org_batch(user, batch_id)
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(batch, key, value)
        if "quantity" in data and "velocity_tag" not in data:
            batch.velocity_tag = classify_velocity(batch.quantity)
        updated = self.repo.update_batch(batch)
        loaded = self.repo.get_batch(updated.id)
        return self._batch_out(loaded or updated)

    def delete_batch(self, user: User, batch_id: UUID) -> None:
        batch = self._get_org_batch(user, batch_id)
        self.repo.delete_batch(batch)

    def _get_org_medicine(self, user: User, medicine_id: UUID) -> Medicine:
        org_id = self._org_id(user)
        medicine = self.repo.get_medicine(medicine_id)
        if not medicine or medicine.organization_id != org_id:
            raise HTTPException(status_code=404, detail="Medicine not found")
        return medicine

    def _get_org_batch(self, user: User, batch_id: UUID) -> StockBatch:
        org_id = self._org_id(user)
        batch = self.repo.get_batch(batch_id)
        if not batch or not batch.medicine or batch.medicine.organization_id != org_id:
            raise HTTPException(status_code=404, detail="Batch not found")
        return batch

    @staticmethod
    def _batch_out(batch: StockBatch) -> BatchOut:
        return BatchOut(
            id=batch.id,
            medicine_id=batch.medicine_id,
            location_id=batch.location_id,
            batch_no=batch.batch_no,
            expiry_date=batch.expiry_date,
            quantity=batch.quantity,
            cold_chain_flag=batch.cold_chain_flag,
            velocity_tag=batch.velocity_tag,
            medicine_name=batch.medicine.name if batch.medicine else None,
            location_name=batch.location.name if batch.location else None,
        )
