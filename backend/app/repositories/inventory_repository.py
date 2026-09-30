from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.inventory import Medicine, StockBatch


class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_medicines(self, organization_id: UUID) -> list[Medicine]:
        return (
            self.db.query(Medicine)
            .filter(Medicine.organization_id == organization_id)
            .order_by(Medicine.name)
            .all()
        )

    def get_medicine(self, medicine_id: UUID) -> Optional[Medicine]:
        return self.db.get(Medicine, medicine_id)

    def create_medicine(self, medicine: Medicine) -> Medicine:
        self.db.add(medicine)
        self.db.commit()
        self.db.refresh(medicine)
        return medicine

    def update_medicine(self, medicine: Medicine) -> Medicine:
        self.db.commit()
        self.db.refresh(medicine)
        return medicine

    def delete_medicine(self, medicine: Medicine) -> None:
        self.db.delete(medicine)
        self.db.commit()

    def list_batches(
        self,
        organization_id: UUID,
        location_id: Optional[UUID] = None,
    ) -> list[StockBatch]:
        query = (
            self.db.query(StockBatch)
            .join(Medicine)
            .options(joinedload(StockBatch.medicine), joinedload(StockBatch.location))
            .filter(Medicine.organization_id == organization_id)
        )
        if location_id:
            query = query.filter(StockBatch.location_id == location_id)
        return query.order_by(StockBatch.expiry_date.asc()).all()

    def get_batch(self, batch_id: UUID) -> Optional[StockBatch]:
        return (
            self.db.query(StockBatch)
            .options(joinedload(StockBatch.medicine), joinedload(StockBatch.location))
            .filter(StockBatch.id == batch_id)
            .first()
        )

    def create_batch(self, batch: StockBatch) -> StockBatch:
        self.db.add(batch)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def update_batch(self, batch: StockBatch) -> StockBatch:
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def delete_batch(self, batch: StockBatch) -> None:
        self.db.delete(batch)
        self.db.commit()
