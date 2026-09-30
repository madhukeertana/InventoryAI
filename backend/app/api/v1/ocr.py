from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas import InvoiceUploadOut
from app.services.ocr_service import OCRService

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post("/invoices", response_model=InvoiceUploadOut)
def upload_invoice(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    file: Annotated[UploadFile, File(...)],
):
    return OCRService(db).process_invoice(current_user, file)
