from crewai import Task

class StrategyTasks:
    def design_strategy(self, agent, business_context):
        return Task(
            description=f"TODO: Implement strategy design logic using context: {business_context}",
            expected_output="A structured JSON strategic plan outlining quarterly objectives.",
            agent=agent
        )
