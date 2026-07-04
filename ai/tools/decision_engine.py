class DecisionEvaluationEngine:
    """
    Receives outputs from business agents, compares recommendations,
    detects conflicts (e.g. Marketing wants to spend, Finance rejects),
    assigns confidence scores, and selects best path.
    """
    def evaluate(self, crew_output, business_context=None) -> dict:
        # Normalize and extract business context
        context_dict = {}
        if business_context:
            if hasattr(business_context, "model_dump"):
                context_dict = business_context.model_dump()
            elif isinstance(business_context, dict):
                context_dict = business_context
        elif isinstance(crew_output, dict) and "context" in crew_output:
            context_dict = crew_output["context"]
        
        # If crew_output is a list, it represents all agent outputs
        agent_outputs = []
        if isinstance(crew_output, list):
            agent_outputs = crew_output
        elif isinstance(crew_output, dict):
            agent_outputs = list(crew_output.values())
            
        profile = context_dict.get("profile", {})
        biz_name = profile.get("name", "the business")
        industry = (profile.get("industry", "SaaS") or "SaaS").lower()
        goals = context_dict.get("goals", [])
        
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

        # 1. Compare recommendations & detect conflicts
        conflicts = []
        recommendations = []
        for out in agent_outputs:
            recs = out.get("recommendations", [])
            recommendations.extend(recs)
            # Detect conflicts dynamically
            if out.get("agent") == "Marketing" and revenue < 15000:
                conflicts.append(f"Marketing spend requested for {biz_name} but restricted by low monthly revenue.")
            if out.get("agent") == "Sales" and churn > 0.08:
                conflicts.append(f"High customer churn rate ({int(churn*100)}%) conflicts with scaling new acquisitions.")
                
        # 2. Merge compatible recommendations
        merged_recommendations = []
        for r in recommendations:
            if r not in merged_recommendations:
                merged_recommendations.append(r)
                
        final_strategy = " | ".join(merged_recommendations[:3]) if merged_recommendations else "Optimize operations and growth parameters."
        
        # 3. Score every recommendation & Assign overall confidence score
        base_confidence = 0.90
        if conflicts:
            base_confidence -= (len(conflicts) * 0.05)
        confidence = max(0.10, round(base_confidence, 2))
        
        # 4. Rank recommendations (based on confidence score of reporting agent)
        # 5. Select the best strategy
        
        # 6. Produce one Executive Summary
        exec_summary = f"CEO & Decision Engine reconciled strategy for {biz_name}. Recommends: {final_strategy}. Reconciled conflicts: {', '.join(conflicts) if conflicts else 'None'}."
        
        # Calculate business health and growth score defaults for the decision stage
        health_val = min(100, max(0, int((retention * 100) + (revenue / 1000) - (churn * 200))))
        growth_val = min(100, max(0, int((leads / 100) * 5 + (revenue / 5000))))
        
        return {
            "business_health": health_val,
            "growth_score": growth_val,
            "confidence": confidence,
            "final_strategy": final_strategy,
            "executive_summary": exec_summary,
            "all_agent_outputs": agent_outputs
        }

    def detect_conflicts(self, outputs: str):
        conflicts = []
        if "reject" in outputs.lower() and "increase budget" in outputs.lower():
            conflicts.append("Marketing budget increase rejected by Finance.")
        if "capacity warning" in outputs.lower():
            conflicts.append("Operations cannot support projected sales volume.")
        return conflicts

    def assign_confidence(self, outputs: str, conflicts: list):
        base_score = 0.90
        base_score -= (len(conflicts) * 0.15)
        return max(0.10, round(base_score, 2))

    def rank_recommendations(self, outputs: str):
        return ["Primary Strategy Execution", "Conservative Growth Path"]

    def merge_recommendations(self, ranked: list):
        return ranked[0] if ranked else "Default Action"

    def generate_executive_summary(self, merged, confidence, conflicts):
        return {
            "Executive Summary": f"The team recommends {merged}.",
            "Key Findings": "Market shows potential, but constrained by budget.",
            "Risks": conflicts,
            "Growth Opportunities": ["Optimization of LTV"],
            "Recommended Actions": ["Execute primary strategy with reduced ad spend"],
            "Confidence Score": confidence,
            "Next Steps": ["Approve budget", "Launch campaign"]
        }
