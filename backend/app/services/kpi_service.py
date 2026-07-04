from ai.tools.kpi_engine import KPIEngine
from app.services.business_context_service import BusinessContextService
from sqlalchemy.orm import Session

class KPIService:
    def __init__(self, db: Session):
        self.kpi_engine = KPIEngine()
        self.context_service = BusinessContextService(db)

    def get_dashboard_data(self, business_id: str):
        context = self.context_service.build_context(business_id)
        metrics = self.kpi_engine.calculate_dashboard_metrics(context.model_dump())
        charts = self.kpi_engine.get_charts_data(context.model_dump())
        return {"metrics": metrics, "charts": charts}
