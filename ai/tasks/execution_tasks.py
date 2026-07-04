from crewai import Task

class ExecutionTasks:
    def plan_marketing_campaign(self, agent, strategy_plan):
        return Task(
            description=f"TODO: Implement marketing campaign logic based on: {strategy_plan}",
            expected_output="A detailed marketing campaign proposal including budget and channels.",
            agent=agent
        )
    
    def review_budget(self, agent, campaign_proposal):
        return Task(
            description=f"TODO: Evaluate the ROI and budget feasibility of the campaign: {campaign_proposal}",
            expected_output="Approval or rejection decision with financial justification.",
            agent=agent
        )
