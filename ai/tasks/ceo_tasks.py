from crewai import Task

class CEOTasks:
    def evaluate_and_approve(self, agent, sub_agent_outputs):
        return Task(
            description=f"TODO: Review all sub-agent outputs and resolve conflicts: {sub_agent_outputs}",
            expected_output="Final executive decision and aggregated recommendations for the user.",
            agent=agent
        )
