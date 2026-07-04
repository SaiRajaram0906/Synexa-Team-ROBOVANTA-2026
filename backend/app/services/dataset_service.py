import csv
from app.schemas.context import BusinessContext
import uuid

class DatasetService:
    def process_csv_dataset(self, file_path: str) -> BusinessContext:
        # Load and parse using built-in csv
        rows = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # clean column headers (strip whitespace)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            for row in reader:
                rows.append(row)
                
        if not rows:
            raise ValueError("CSV file is empty")
            
        headers = list(rows[0].keys())
        required_cols = [
            'base_price', 'marketing_spend', 'forecasted_demand', 
            'actual_demand', 'closing_inventory', 'customer_satisfaction_score'
        ]
        missing = [col for col in required_cols if col not in headers]
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

        # Clean row values helper
        def get_float(row, col, default=0.0):
            val = row.get(col)
            if val is None or val.strip() == "":
                return default
            try:
                return float(val)
            except ValueError:
                return default
                
        def get_int(row, col, default=0):
            val = row.get(col)
            if val is None or val.strip() == "":
                return default
            try:
                return int(float(val))
            except ValueError:
                return default

        # Aggregate variables
        categories = {}
        lifecycle_stages = {}
        variant_counts = []
        
        marketing_spends = []
        promotion_intensity_scores = []
        promo_types = {}
        discount_percents = []
        competitor_price_indices = []
        
        forecasted_demands = []
        actual_demands = []
        
        closing_inventories = []
        stockout_flags = []
        backorder_quantities = []
        emergency_restock_costs = []
        inventory_holding_costs = []
        
        warehouse_distances = []
        delivery_lead_times = []
        order_fulfillment_rates = []
        
        customer_satisfaction_scores = []
        quality_return_rates = []
        base_prices = []

        for row in rows:
            # 1. Product
            cat = row.get('product_category', 'General')
            categories[cat] = categories.get(cat, 0) + 1
            
            stage = row.get('product_lifecycle_stage', '')
            if stage:
                lifecycle_stages[stage] = lifecycle_stages.get(stage, 0) + 1
                
            variant_counts.append(get_int(row, 'product_variant_count', 0))
            
            # 2. Marketing
            marketing_spends.append(get_float(row, 'marketing_spend', 0.0))
            promotion_intensity_scores.append(get_float(row, 'promotion_intensity_score', 50.0))
            ptype = row.get('promotion_type', '')
            if ptype:
                promo_types[ptype] = promo_types.get(ptype, 0) + 1
            discount_percents.append(get_float(row, 'discount_percent', 0.0))
            competitor_price_indices.append(get_float(row, 'competitor_price_index', 1.0))
            
            # 3. Sales
            forecasted_demands.append(get_float(row, 'forecasted_demand', 0.0))
            actual_demands.append(get_float(row, 'actual_demand', 0.0))
            
            # 4. Inventory
            closing_inventories.append(get_float(row, 'closing_inventory', 0.0))
            stockout_flags.append(get_int(row, 'stockout_flag', 0))
            backorder_quantities.append(get_float(row, 'backorder_quantity', 0.0))
            emergency_restock_costs.append(get_float(row, 'emergency_restock_cost', 0.0))
            inventory_holding_costs.append(get_float(row, 'inventory_holding_cost', 0.0))
            
            # 5. Supply Chain
            warehouse_distances.append(get_float(row, 'warehouse_distance_km', 100.0))
            delivery_lead_times.append(get_float(row, 'delivery_lead_time_days', 5))
            order_fulfillment_rates.append(get_float(row, 'order_fulfillment_rate', 1.0))
            
            # 6. Customer Success
            customer_satisfaction_scores.append(get_float(row, 'customer_satisfaction_score', 3.5))
            quality_return_rates.append(get_float(row, 'quality_return_rate', 0.0))
            
            # 7. Base price
            base_prices.append(get_float(row, 'base_price', 0.0))

        # Calculate averages
        def safe_mean(lst):
            return sum(lst) / len(lst) if lst else 0.0

        total_mkt_spend = sum(marketing_spends)
        avg_mkt_spend = safe_mean(marketing_spends)
        avg_promo_intensity = safe_mean(promotion_intensity_scores)
        avg_discount = safe_mean(discount_percents)
        avg_competitor_index = safe_mean(competitor_price_indices)
        
        total_forecasted_demand = sum(forecasted_demands)
        total_actual_demand = sum(actual_demands)
        
        # Calculate forecast accuracy
        abs_diff_sum = sum(abs(a - f) for a, f in zip(actual_demands, forecasted_demands))
        actual_sum = sum(actual_demands)
        if actual_sum > 0:
            accuracy = 100.0 * (1.0 - abs_diff_sum / actual_sum)
        else:
            accuracy = 90.0

        avg_closing_inventory = safe_mean(closing_inventories)
        total_stockouts = sum(stockout_flags)
        avg_holding_cost = safe_mean(inventory_holding_costs)
        total_backorder = sum(backorder_quantities)
        avg_restock_cost = safe_mean(emergency_restock_costs)
        
        avg_distance = safe_mean(warehouse_distances)
        avg_lead_time = safe_mean(delivery_lead_times)
        avg_fulfillment = safe_mean(order_fulfillment_rates)
        
        avg_csat = safe_mean(customer_satisfaction_scores)
        avg_quality_return = safe_mean(quality_return_rates)
        avg_base_price = safe_mean(base_prices)
        avg_variants = safe_mean(variant_counts)

        current_kpis = {
            "product_performance": {
                "categories": categories,
                "lifecycle_stages": lifecycle_stages,
                "avg_variant_count": avg_variants
            },
            "marketing_performance": {
                "total_spend": total_mkt_spend,
                "avg_spend": avg_mkt_spend,
                "avg_intensity": avg_promo_intensity,
                "promo_types": promo_types,
                "avg_discount_percent": avg_discount
            },
            "sales_performance": {
                "total_forecasted_demand": total_forecasted_demand,
                "total_actual_demand": total_actual_demand,
                "accuracy_percent": max(0.0, min(100.0, accuracy))
            },
            "inventory_health": {
                "avg_closing_inventory": avg_closing_inventory,
                "total_stockouts": total_stockouts,
                "avg_holding_cost": avg_holding_cost,
                "total_backorder": total_backorder,
                "avg_emergency_restock_cost": avg_restock_cost
            },
            "supply_chain_health": {
                "avg_warehouse_distance_km": avg_distance,
                "avg_delivery_lead_time_days": avg_lead_time,
                "avg_order_fulfillment_rate": avg_fulfillment
            },
            "customer_satisfaction": {
                "avg_satisfaction_score": avg_csat,
                "avg_quality_return_rate": avg_quality_return
            },
            "pricing_insights": {
                "avg_base_price": avg_base_price,
                "avg_competitor_price_index": avg_competitor_index
            }
        }
        
        context = BusinessContext(
            business_id=str(uuid.uuid4()),
            profile={
                "name": "Uploaded CSV Dataset",
                "industry": "Multi-category General Retail",
                "total_records": len(rows)
            },
            goals=[{"description": "Optimize pricing, marketing efficiency, and supply chain margins based on CSV signals."}],
            documents_summary="Parsed uploaded business performance CSV dataset.",
            current_kpis=current_kpis,
            previous_strategies=[],
            campaign_history=[],
            recommendations=[],
            customer_history={},
            memory_context="No prior memory, starting analysis cycle from dataset upload.",
            knowledge_context="Dataset contains categories: " + ", ".join(list(categories.keys())[:3])
        )
        
        return context
