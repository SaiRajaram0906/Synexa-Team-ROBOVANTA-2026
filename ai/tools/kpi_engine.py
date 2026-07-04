class KPIEngine:
    def calculate_scores_from_decision(self, decision: dict, context_dict: dict) -> dict:
        # Consume Decision Engine output
        confidence = decision.get("confidence", 0.90)
        final_strategy = decision.get("final_strategy", "")
        
        # Extract context variables for deterministic business formulas
        kpis = context_dict.get("current_kpis", {})
        revenue = kpis.get("current_revenue", 0)
        if not revenue:
            revenue = kpis.get("revenue", 0)
        leads = kpis.get("leads", 0)
        retention = kpis.get("customer_retention", 0.8)
        if not retention:
            retention = kpis.get("retention", 0.8)
        churn = kpis.get("churn_rate", 0.1)
        if not churn:
            churn = kpis.get("churn", 0.1)
            
        # Business Health = (retention * 100) + (revenue / 1000) - (churn * 200) adjusted by confidence
        base_health = (retention * 100) + (revenue / 1000) - (churn * 200)
        health_score = min(100, max(0, int(base_health * confidence)))
        
        # Growth Score = ((leads / 100) * 5 + (revenue / 5000)) adjusted by confidence
        base_growth = (leads / 100) * 5 + (revenue / 5000)
        growth_score = min(100, max(0, int(base_growth * confidence)))
        
        # Revenue Opportunity = Projected additional revenue based on strategy impact
        rev_opp = revenue * 0.20 * retention
        
        # Lead Score
        lead_score = "High" if leads > 500 else ("Medium" if leads > 100 else "Low")
        
        # Customer Health
        cust_health = int((1 - churn) * 100)
        
        # Market Readiness
        market_readiness = "Ready" if health_score > 60 else "Not Ready"
        
        # Risk Alerts count
        risks = 0
        if churn > 0.12: risks += 1
        if revenue < 10000: risks += 1
        if health_score < 55: risks += 1
        
        return {
            "business_health": {"value": health_score, "trend": "up" if health_score > 70 else "down", "confidence": confidence},
            "growth_score": {"value": growth_score, "trend": "up" if growth_score > 60 else "neutral", "confidence": confidence},
            "revenue_opportunity": {"value": round(rev_opp, 2), "trend": "up", "confidence": confidence},
            "lead_score": {"value": lead_score, "trend": "neutral", "confidence": confidence},
            "customer_health": {"value": cust_health, "trend": "up" if cust_health > 80 else "down", "confidence": confidence},
            "market_readiness": {"value": market_readiness, "trend": "up", "confidence": confidence},
            "risk_alerts": {"value": risks, "trend": "up" if risks > 1 else "down", "confidence": confidence},
            "executive_summary": f"KPI calculations complete for strategy: '{final_strategy[:50]}...'. Calculated health score is {health_score}/100 and growth potential is {growth_score}/100."
        }

    def calculate_dashboard_metrics(self, business_context: dict) -> dict:
        # Maintain backward compatibility
        return self.calculate_scores_from_decision({}, business_context)
    
    def get_charts_data(self, business_context: dict) -> dict:
        kpis = business_context.get("current_kpis", {})
        
        mkt = kpis.get("marketing_performance", {})
        sales = kpis.get("sales_performance", {})
        inv = kpis.get("inventory_health", {})
        sc = kpis.get("supply_chain_health", {})
        cust = kpis.get("customer_satisfaction", {})
        pricing = kpis.get("pricing_insights", {})

        actual = sales.get("total_actual_demand", 10000.0)
        forecast = sales.get("total_forecasted_demand", 10000.0)
        price = pricing.get("avg_base_price", 10.0)
        revenue = actual * price
        
        # 1. Revenue Trend
        revenue_trend = [
            {'name': 'Q1', 'revenue': round(revenue * 0.2, 2), 'leads': round(actual * 0.22, 0)},
            {'name': 'Q2', 'revenue': round(revenue * 0.25, 2), 'leads': round(actual * 0.28, 0)},
            {'name': 'Q3', 'revenue': round(revenue * 0.3, 2), 'leads': round(actual * 0.32, 0)},
            {'name': 'Q4', 'revenue': round(revenue * 0.25, 2), 'leads': round(actual * 0.26, 0)},
        ]
        
        # 2. Demand Forecast
        demand_forecast = [
            {'name': 'Segment A', 'forecasted': round(forecast * 0.2, 0), 'actual': round(actual * 0.19, 0)},
            {'name': 'Segment B', 'forecasted': round(forecast * 0.25, 0), 'actual': round(actual * 0.26, 0)},
            {'name': 'Segment C', 'forecasted': round(forecast * 0.35, 0), 'actual': round(actual * 0.33, 0)},
            {'name': 'Segment D', 'forecasted': round(forecast * 0.2, 0), 'actual': round(actual * 0.22, 0)},
        ]
        
        # 3. Marketing Performance
        total_spend = mkt.get("total_spend", 0.0)
        promo_types = mkt.get("promo_types", {})
        marketing_performance = []
        if promo_types:
            for k, v in promo_types.items():
                marketing_performance.append({'name': k, 'spend': round(total_spend * (v / sum(promo_types.values())), 2)})
        else:
            marketing_performance = [
                {'name': 'Discount', 'spend': round(total_spend * 0.4, 2)},
                {'name': 'Bundle', 'spend': round(total_spend * 0.35, 2)},
                {'name': 'BOGO', 'spend': round(total_spend * 0.25, 2)},
            ]
            
        # 4. Inventory Health
        closing = inv.get("avg_closing_inventory", 0.0)
        backorder = inv.get("total_backorder", 0.0)
        inventory_health = [
            {'name': 'Opening', 'value': round(closing * 1.2, 2)},
            {'name': 'Closing', 'value': round(closing, 2)},
            {'name': 'Backorder', 'value': round(backorder, 2)},
        ]
        
        # 5. Supply Chain Performance
        lead_time = sc.get("avg_delivery_lead_time_days", 0.0)
        distance = sc.get("avg_warehouse_distance_km", 0.0)
        fulfillment = sc.get("avg_order_fulfillment_rate", 1.0)
        supply_chain_performance = [
            {'name': 'Lead Time (Days)', 'value': round(lead_time, 2)},
            {'name': 'Distance (100km)', 'value': round(distance / 100.0, 2)},
            {'name': 'Fulfillment (%)', 'value': round(fulfillment * 100.0, 2)},
        ]
        
        # 6. Customer Satisfaction
        csat = cust.get("avg_satisfaction_score", 0.0)
        returns = cust.get("avg_quality_return_rate", 0.0)
        customer_satisfaction = [
            {'name': 'CSAT Score (x20)', 'value': round(csat * 20.0, 2)},
            {'name': 'Quality Return Rate (%)', 'value': round(returns * 100.0, 2)},
        ]
        
        return {
            "revenue_trend": revenue_trend,
            "demand_forecast": demand_forecast,
            "marketing_performance": marketing_performance,
            "inventory_health": inventory_health,
            "supply_chain_performance": supply_chain_performance,
            "customer_satisfaction": customer_satisfaction
        }
