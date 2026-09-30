"""Seed organizations, locations, users (all roles), and sample inventory."""

from datetime import date, timedelta

from app.core.config import get_settings
from app.core.db import Base, SessionLocal, engine
from app.core.dependencies import Role
from app.core.security import hash_password
import app.models  # noqa: F401
from app.models.inventory import Medicine, StockBatch
from app.models.organization import Location, Organization
from app.models.user import User

settings = get_settings()
DEFAULT_PASSWORD = "Password123!"


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == settings.seed_admin_email).first():
            print("Seed already applied — skipping")
            return

        platform = Organization(
            name="PharmaStock Platform",
            org_type="PLATFORM",
            drug_license_no=None,
            license_expiry=None,
        )
        retail = Organization(
            name="Sri Venkateswara Medical Stores",
            org_type="RETAIL",
            drug_license_no="DL-RET-2024-8891",
            license_expiry=date.today() + timedelta(days=45),
        )
        distributor = Organization(
            name="Patel Pharma Wholesale Hub",
            org_type="DISTRIBUTOR",
            drug_license_no="DL-DIST-2022-4410",
            license_expiry=date.today() + timedelta(days=400),
        )
        hospital = Organization(
            name="Gachibowli Care Hospital Pharmacy",
            org_type="HOSPITAL",
            drug_license_no="DL-HOSP-2023-1122",
            license_expiry=date.today() + timedelta(days=200),
        )
        chain = Organization(
            name="Nair Local Pharmacy Chain",
            org_type="CHAIN",
            drug_license_no="DL-CHN-2021-7788",
            license_expiry=date.today() + timedelta(days=120),
        )
        db.add_all([platform, retail, distributor, hospital, chain])
        db.flush()

        store = Location(
            organization_id=retail.id, name="Kukatpally Store", location_type="STORE"
        )
        warehouse = Location(
            organization_id=distributor.id,
            name="Secunderabad Warehouse",
            location_type="WAREHOUSE",
        )
        icu = Location(
            organization_id=hospital.id, name="ICU Pharmacy", location_type="ICU"
        )
        branch1 = Location(
            organization_id=chain.id, name="IT Corridor Outlet", location_type="BRANCH"
        )
        branch2 = Location(
            organization_id=chain.id, name="Old City Outlet", location_type="BRANCH"
        )
        db.add_all([store, warehouse, icu, branch1, branch2])
        db.flush()

        users = [
            User(
                email=settings.seed_admin_email.lower(),
                password_hash=hash_password(settings.seed_admin_password),
                full_name="System Admin",
                role=Role.SYSTEM_ADMIN,
                organization_id=platform.id,
                location_id=None,
            ),
            User(
                email="owner@retail.example",
                password_hash=hash_password(DEFAULT_PASSWORD),
                full_name="Ravi Reddy",
                role=Role.PHARMACY_OWNER,
                organization_id=retail.id,
                location_id=store.id,
            ),
            User(
                email="manager@retail.example",
                password_hash=hash_password(DEFAULT_PASSWORD),
                full_name="Sneha Rao",
                role=Role.STORE_MANAGER,
                organization_id=retail.id,
                location_id=store.id,
            ),
            User(
                email="procurement@dist.example",
                password_hash=hash_password(DEFAULT_PASSWORD),
                full_name="Karthik Sharma",
                role=Role.PROCUREMENT_MANAGER,
                organization_id=distributor.id,
                location_id=warehouse.id,
            ),
            User(
                email="hospital@hosp.example",
                password_hash=hash_password(DEFAULT_PASSWORD),
                full_name="Dr. Meena Iyer",
                role=Role.HOSPITAL_INCHARGE,
                organization_id=hospital.id,
                location_id=icu.id,
            ),
            User(
                email="warehouse@dist.example",
                password_hash=hash_password(DEFAULT_PASSWORD),
                full_name="Imran Khan",
                role=Role.WAREHOUSE_BRANCH_MANAGER,
                organization_id=distributor.id,
                location_id=warehouse.id,
            ),
            User(
                email="chainhead@chain.example",
                password_hash=hash_password(DEFAULT_PASSWORD),
                full_name="Priya Nair",
                role=Role.MULTI_OUTLET_INVENTORY_HEAD,
                organization_id=chain.id,
                location_id=None,
            ),
        ]
        db.add_all(users)
        db.flush()

        meds = [
            Medicine(
                organization_id=retail.id,
                name="Amoxicillin 500mg",
                sku="AMOX-500",
                requires_cold_chain=False,
            ),
            Medicine(
                organization_id=retail.id,
                name="Insulin Glargine",
                sku="INS-GLAR",
                requires_cold_chain=True,
            ),
            Medicine(
                organization_id=retail.id,
                name="Paracetamol 650",
                sku="PCM-650",
                requires_cold_chain=False,
            ),
        ]
        db.add_all(meds)
        db.flush()

        batches = [
            StockBatch(
                medicine_id=meds[0].id,
                location_id=store.id,
                batch_no="AX-2401",
                expiry_date=date.today() + timedelta(days=25),
                quantity=18,
                cold_chain_flag=False,
                velocity_tag="FAST",
            ),
            StockBatch(
                medicine_id=meds[1].id,
                location_id=store.id,
                batch_no="IG-8802",
                expiry_date=date.today() + timedelta(days=90),
                quantity=40,
                cold_chain_flag=True,
                velocity_tag="MEDIUM",
            ),
            StockBatch(
                medicine_id=meds[2].id,
                location_id=store.id,
                batch_no="PC-1109",
                expiry_date=date.today() + timedelta(days=200),
                quantity=220,
                cold_chain_flag=False,
                velocity_tag="SLOW",
            ),
            StockBatch(
                medicine_id=meds[0].id,
                location_id=store.id,
                batch_no="AX-OLD",
                expiry_date=date.today() + timedelta(days=12),
                quantity=8,
                cold_chain_flag=False,
                velocity_tag="FAST",
            ),
        ]
        db.add_all(batches)

        # Chain sample stock
        chain_med = Medicine(
            organization_id=chain.id,
            name="Cetirizine 10mg",
            sku="CET-10",
            requires_cold_chain=False,
        )
        db.add(chain_med)
        db.flush()
        db.add(
            StockBatch(
                medicine_id=chain_med.id,
                location_id=branch1.id,
                batch_no="CET-01",
                expiry_date=date.today() + timedelta(days=40),
                quantity=15,
                cold_chain_flag=False,
                velocity_tag="FAST",
            )
        )

        db.commit()
        print("Seed complete.")
        print(f"Admin: {settings.seed_admin_email} / {settings.seed_admin_password}")
        print(f"Demo users password: {DEFAULT_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
