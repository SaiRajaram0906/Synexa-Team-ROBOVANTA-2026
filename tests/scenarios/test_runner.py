import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ai.tools.decision_engine import DecisionEvaluationEngine
from ai.tools.kpi_engine import KPIEngine
from tests.scenarios.test_scenarios import SCENARIOS

def run_tests():
    decision_engine = DecisionEvaluationEngine()
    kpi_engine = KPIEngine()
    
    print("Running End-to-End KPI and Decision Engine Tests on Sample Scenarios...")
    
    for name, data in SCENARIOS.items():
        print(f"\n--- Testing Scenario: {name.upper()} ---")
        
        # 1. Test KPI Engine
        context_mock = {"current_kpis": data["kpis"]}
        kpis = kpi_engine.calculate_dashboard_metrics(context_mock)
        print(f"Business Health: {kpis['business_health']['value']}")
        print(f"Risk Alerts: {kpis['risk_alerts']['value']}")
        
        # 2. Test Decision Engine
        # We simulate a crew output string containing some keywords
        simulated_crew_output = f"Marketing wants to increase budget. Finance might reject. Capacity warning."
        decision = decision_engine.evaluate(simulated_crew_output)
        
        print(f"Conflicts Detected: {decision['conflicts_detected']}")
        print(f"Confidence Score: {decision['confidence_score']}")
        print(f"Executive Summary: {decision['executive_summary']['Executive Summary']}")
        
if __name__ == '__main__':
    run_tests()
