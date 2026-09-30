from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas import (
    BatchCreate,
    BatchOut,
    BatchUpdate,
    MedicineCreate,
    MedicineOut,
    MedicineUpdate,
    MessageOut,
)
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/medicines", response_model=list[MedicineOut])
def list_medicines(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return InventoryService(db).list_medicines(current_user)


@router.post("/medicines", response_model=MedicineOut, status_code=status.HTTP_201_CREATED)
def create_medicine(
    payload: MedicineCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return InventoryService(db).create_medicine(current_user, payload)


@router.patch("/medicines/{medicine_id}", response_model=MedicineOut)
def update_medicine(
    medicine_id: UUID,
    payload: MedicineUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return InventoryService(db).update_medicine(current_user, medicine_id, payload)


@router.delete("/medicines/{medicine_id}", response_model=MessageOut)
def delete_medicine(
    medicine_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    InventoryService(db).delete_medicine(current_user, medicine_id)
    return MessageOut(message="Medicine deleted")


@router.get("/batches", response_model=list[BatchOut])
def list_batches(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return InventoryService(db).list_batches(current_user)


@router.post("/batches", response_model=BatchOut, status_code=status.HTTP_201_CREATED)
def create_batch(
    payload: BatchCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return InventoryService(db).create_batch(current_user, payload)


@router.patch("/batches/{batch_id}", response_model=BatchOut)
def update_batch(
    batch_id: UUID,
    payload: BatchUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return InventoryService(db).update_batch(current_user, batch_id, payload)


@router.delete("/batches/{batch_id}", response_model=MessageOut)
def delete_batch(
    batch_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    InventoryService(db).delete_batch(current_user, batch_id)
    return MessageOut(message="Batch deleted")
