from datetime import date
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str
    role: str
    organization_id: UUID
    location_id: Optional[UUID] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str
    role: str
    organization_id: Optional[UUID]
    location_id: Optional[UUID]
    is_active: bool


class MedicineCreate(BaseModel):
    name: str
    sku: str
    requires_cold_chain: bool = False


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    requires_cold_chain: Optional[bool] = None


class MedicineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    sku: str
    requires_cold_chain: bool


class BatchCreate(BaseModel):
    medicine_id: UUID
    location_id: UUID
    batch_no: str
    expiry_date: date
    quantity: int = Field(ge=0)
    cold_chain_flag: bool = False
    velocity_tag: Optional[str] = "UNKNOWN"


class BatchUpdate(BaseModel):
    batch_no: Optional[str] = None
    expiry_date: Optional[date] = None
    quantity: Optional[int] = Field(default=None, ge=0)
    cold_chain_flag: Optional[bool] = None
    velocity_tag: Optional[str] = None
    location_id: Optional[UUID] = None


class BatchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    medicine_id: UUID
    location_id: UUID
    batch_no: str
    expiry_date: date
    quantity: int
    cold_chain_flag: bool
    velocity_tag: Optional[str]
    medicine_name: Optional[str] = None
    location_name: Optional[str] = None


class ActionCardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    assignee_user_id: Optional[UUID]
    card_type: str
    status: str
    reason: str
    payload: Optional[dict[str, Any]]
    action_date: date


class ActionCardUpdate(BaseModel):
    status: str = Field(pattern="^(ACCEPTED|OVERRIDDEN|DISMISSED)$")


class InvoiceUploadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    uploaded_by: UUID
    file_path: str
    parse_status: str
    parsed_payload: Optional[dict[str, Any]]
    created_batches: list[BatchOut] = []


class MessageOut(BaseModel):
    message: str
