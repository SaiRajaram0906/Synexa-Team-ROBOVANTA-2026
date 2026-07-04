from crewai import Task
from ai.prompts.strategy_prompt import TASK_PROMPT, OUTPUT_FORMAT

class StrategyTasks:
    def design_strategy(self, agent, context):
        return Task(
            description=f"{TASK_PROMPT}\nContext: {context}",
            expected_output=OUTPUT_FORMAT,
            agent=agent
        )
