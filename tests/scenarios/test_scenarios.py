# Sample Business Scenarios for MVP Demo
SCENARIOS = {
    "retail_store": {
        "profile": {"name": "Lumina Apparel", "industry": "Retail", "type": "B2C"},
        "goals": ["Increase foot traffic by 20%", "Clear winter inventory"],
        "kpis": {"current_revenue": 45000, "customer_retention": 0.45},
        "expected_flow": "Strategy -> Marketing (Local Ads) -> Ops (Inventory) -> Finance (Budget)"
    },
    "restaurant": {
        "profile": {"name": "The Rustic Spoon", "industry": "Food & Beverage", "type": "B2C"},
        "goals": ["Boost weekday lunch sales", "Improve online reviews"],
        "kpis": {"current_revenue": 30000, "table_turnover": 45},
        "expected_flow": "Strategy -> Marketing (Social) -> Customer Success (Reviews) -> Finance"
    },
    "gym": {
        "profile": {"name": "IronCore Fitness", "industry": "Health & Wellness", "type": "B2C"},
        "goals": ["Acquire 50 new members this month", "Reduce churn"],
        "kpis": {"current_revenue": 25000, "churn_rate": 0.08},
        "expected_flow": "Strategy -> Marketing (Promo) -> Sales (Conversion) -> Customer Success"
    },
    "ecommerce": {
        "profile": {"name": "TechHaven", "industry": "E-commerce", "type": "B2C"},
        "goals": ["Increase average order value", "Reduce cart abandonment"],
        "kpis": {"current_revenue": 120000, "cart_abandonment": 0.65},
        "expected_flow": "Strategy -> Marketing (Email Drip) -> Ops (Fulfillment) -> Finance"
    },
    "healthcare": {
        "profile": {"name": "Vitality Clinic", "industry": "Healthcare", "type": "B2C"},
        "goals": ["Increase patient bookings", "Improve patient follow-ups"],
        "kpis": {"current_revenue": 80000, "no_show_rate": 0.15},
        "expected_flow": "Strategy -> Ops (Scheduling) -> Customer Success (Follow-ups) -> Finance"
    },
    "startup": {
        "profile": {"name": "SaaSify", "industry": "Software", "type": "B2B"},
        "goals": ["Secure 5 enterprise pilots", "Achieve $10k MRR"],
        "kpis": {"current_mrr": 4500, "cac": 120},
        "expected_flow": "Strategy -> Marketing (Content) -> Sales (Outreach) -> Finance (Burn Rate)"
    }
}
