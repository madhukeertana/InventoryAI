from datetime import date
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import Role
from app.models.inventory import Medicine, StockBatch
from app.models.ocr import InvoiceUpload
from app.models.user import User
from app.repositories.action_card_repository import InvoiceRepository
from app.repositories.inventory_repository import InventoryRepository
from app.rules.inventory_rules import classify_velocity
from app.schemas import BatchOut, InvoiceUploadOut
from app.services.inventory_service import InventoryService

settings = get_settings()


class OCRService:
    """MVP stub: stores file and returns deterministic parsed invoice fields."""

    def __init__(self, db: Session):
        self.db = db
        self.invoice_repo = InvoiceRepository(db)
        self.inventory_repo = InventoryRepository(db)

    def process_invoice(self, user: User, file: UploadFile) -> InvoiceUploadOut:
        if not user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has no organization",
            )
        if not user.location_id and user.role not in {
            Role.SYSTEM_ADMIN,
            Role.MULTI_OUTLET_INVENTORY_HEAD,
        }:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has no location for inward stock",
            )

        upload_root = Path(settings.ocr_upload_dir)
        upload_root.mkdir(parents=True, exist_ok=True)
        suffix = Path(file.filename or "invoice.bin").suffix or ".bin"
        stored_name = f"{uuid4()}{suffix}"
        dest = upload_root / stored_name
        content = file.file.read()
        dest.write_bytes(content)

        parsed = self._stub_parse(file.filename or stored_name)
        location_id = user.location_id or self._fallback_location(user.organization_id)
        if not location_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No location available for stock inward",
            )

        medicine = (
            self.db.query(Medicine)
            .filter(
                Medicine.organization_id == user.organization_id,
                Medicine.sku == parsed["sku"],
            )
            .first()
        )
        if not medicine:
            medicine = Medicine(
                organization_id=user.organization_id,
                name=parsed["medicine_name"],
                sku=parsed["sku"],
                requires_cold_chain=parsed["requires_cold_chain"],
            )
            self.db.add(medicine)
            self.db.flush()

        batch = StockBatch(
            medicine_id=medicine.id,
            location_id=location_id,
            batch_no=parsed["batch_no"],
            expiry_date=date.fromisoformat(parsed["expiry_date"]),
            quantity=parsed["quantity"],
            cold_chain_flag=parsed["requires_cold_chain"],
            velocity_tag=classify_velocity(parsed["quantity"]),
        )
        self.db.add(batch)
        self.db.flush()

        upload = InvoiceUpload(
            organization_id=user.organization_id,
            uploaded_by=user.id,
            file_path=str(dest),
            parse_status="PARSED_STUB",
            parsed_payload=parsed,
        )
        saved = self.invoice_repo.create(upload)
        loaded = self.inventory_repo.get_batch(batch.id)
        batch_out = InventoryService._batch_out(loaded or batch)
        return InvoiceUploadOut(
            id=saved.id,
            organization_id=saved.organization_id,
            uploaded_by=saved.uploaded_by,
            file_path=saved.file_path,
            parse_status=saved.parse_status,
            parsed_payload=saved.parsed_payload,
            created_batches=[batch_out],
        )

    def _fallback_location(self, organization_id: UUID) -> UUID | None:
        from app.models.organization import Location

        loc = (
            self.db.query(Location)
            .filter(Location.organization_id == organization_id)
            .first()
        )
        return loc.id if loc else None

    @staticmethod
    def _stub_parse(filename: str) -> dict:
        today = date.today()
        return {
            "medicine_name": "Amoxicillin 500mg",
            "sku": "AMOX-500",
            "batch_no": f"STUB-{filename[:8].upper()}",
            "expiry_date": (today.replace(year=today.year + 1)).isoformat()
            if today.month < 12
            else date(today.year + 1, 12, 28).isoformat(),
            "quantity": 120,
            "requires_cold_chain": "cold" in filename.lower() or "fridge" in filename.lower(),
            "storage_temp": "2-8C" if "cold" in filename.lower() else "ambient",
            "engine": "tesseract-stub",
        }
