import os
import uuid
from datetime import datetime, timezone
import sys

# Add backend and root directories to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from app.db import SessionLocal
from app.models.domain import User, Business, BusinessDocument, Strategy, KPIMetric
from database.seed_data import DEMO_BUSINESSES

def seed():
    db = SessionLocal()
    try:
        # 1. Create default user
        user_id = "00000000-0000-0000-0000-000000000000"
        user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if not user:
            user = User(id=uuid.UUID(user_id), email="demo@synexa.com")
            db.add(user)
            db.commit()
            print("Demo user created.")
        else:
            print("Demo user already exists.")

        # 2. Insert businesses and related data
        for b_data in DEMO_BUSINESSES:
            b_id = uuid.UUID(b_data["id"])
            existing_business = db.query(Business).filter(Business.id == b_id).first()
            if not existing_business:
                # Create business
                business = Business(
                    id=b_id,
                    user_id=uuid.UUID(user_id),
                    name=b_data["name"],
                    industry=b_data["industry"],
                    profile_summary=f"Demo profile for {b_data['name']}"
                )
                db.add(business)
                
                # Create KPI metrics
                kpis = b_data.get("kpis", {})
                for k, v in kpis.items():
                    kpi = KPIMetric(
                        id=uuid.uuid4(),
                        business_id=b_id,
                        metric_name=k,
                        value=float(v),
                        recorded_at=datetime.now(timezone.utc)
                    )
                    db.add(kpi)
                
                # Create Strategy/Goals
                goals = b_data.get("goals", [])
                if goals:
                    strat = Strategy(
                        id=uuid.uuid4(),
                        business_id=b_id,
                        goals=goals,
                        status="active"
                    )
                    db.add(strat)

                # Create BusinessDocuments
                docs = b_data.get("documents", [])
                for doc_data in docs:
                    doc = BusinessDocument(
                        id=uuid.uuid4(),
                        business_id=b_id,
                        type=doc_data.get("name", "Document"),
                        status="pending"
                    )
                    db.add(doc)
                
                db.commit()
                print(f"Seeded business: {b_data['name']}")
            else:
                print(f"Business already exists: {b_data['name']}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
