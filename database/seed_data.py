import uuid
from datetime import datetime

DEMO_BUSINESSES = [
    {
        "id": str(uuid.uuid4()),
        "name": "The Rustic Spoon",
        "industry": "Restaurant",
        "kpis": {"revenue": 30000, "table_turnover": 45},
        "goals": ["Boost weekday lunch sales"],
        "documents": [{"name": "Q1_Sales.pdf", "content": "Sample content"}]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Lumina Apparel",
        "industry": "Retail",
        "kpis": {"revenue": 45000, "customer_retention": 0.45},
        "goals": ["Clear winter inventory"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "IronCore Fitness",
        "industry": "Gym",
        "kpis": {"revenue": 25000, "churn_rate": 0.08},
        "goals": ["Acquire 50 new members"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Vitality Clinic",
        "industry": "Healthcare",
        "kpis": {"revenue": 80000, "no_show_rate": 0.15},
        "goals": ["Increase patient bookings"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "TechHaven",
        "industry": "E-commerce",
        "kpis": {"revenue": 120000, "cart_abandonment": 0.65},
        "goals": ["Reduce cart abandonment"]
    },
    {
        "id": str(uuid.uuid4()),
        "name": "SaaSify",
        "industry": "Startup",
        "kpis": {"mrr": 4500, "cac": 120},
        "goals": ["Secure 5 enterprise pilots"]
    }
]
