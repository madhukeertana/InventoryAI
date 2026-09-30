import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    requires_cold_chain: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    batches: Mapped[list["StockBatch"]] = relationship(back_populates="medicine")


class StockBatch(Base):
    __tablename__ = "stock_batches"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    medicine_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medicines.id"), nullable=False, index=True
    )
    location_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("locations.id"), nullable=False, index=True
    )
    batch_no: Mapped[str] = mapped_column(String(100), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cold_chain_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    velocity_tag: Mapped[Optional[str]] = mapped_column(String(20), default="UNKNOWN")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    medicine: Mapped["Medicine"] = relationship(back_populates="batches")
    location = relationship("Location")
