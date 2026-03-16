from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.subscription import SubscriptionPlan

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("/seed")
def seed_plans(db: Session = Depends(get_db)):
    plans = [
        {
            "name": "Free",
            "price": 0,
            "max_users": 5,
            "max_projects": 3,
        },
        {
            "name": "Pro",
            "price": 2000,
            "max_users": 25,
            "max_projects": 20,
        },
        {
            "name": "Enterprise",
            "price": 10000,
            "max_users": None,
            "max_projects": None,
        },
    ]

    created = []

    for plan in plans:
        exists = (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.name == plan["name"])
            .first()
        )

        if not exists:
            new_plan = SubscriptionPlan(**plan)
            db.add(new_plan)
            created.append(plan["name"])

    db.commit()

    return {"seeded_plans": created}
