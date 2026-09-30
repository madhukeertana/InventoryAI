"""Stub Drug License Verification API client."""

from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.organization import Organization

settings = get_settings()


class LicenseService:
    def check_org_license(self, db: Session, organization_id: UUID) -> dict | None:
        org = db.get(Organization, organization_id)
        if not org:
            return None
        if not org.license_expiry:
            return {
                "valid": False,
                "reason": "Drug license expiry not on file — verify before dispatch",
                "engine": "license-api-stub",
                "api_configured": bool(settings.drug_license_api_url),
            }
        days = (org.license_expiry - date.today()).days
        if days < 0:
            return {
                "valid": False,
                "reason": f"Drug license {org.drug_license_no or ''} expired — block dispatch",
                "engine": "license-api-stub",
                "days_overdue": abs(days),
            }
        if days <= 60:
            return {
                "valid": True,
                "reason": f"Drug license renews in {days} days — pre-billing firewall warning",
                "engine": "license-api-stub",
                "days_remaining": days,
            }
        return None
