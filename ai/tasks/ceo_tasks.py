from crewai import Task
from ai.prompts.ceo_prompt import TASK_PROMPT, OUTPUT_FORMAT

class CEOTasks:
    def orchestrate_and_summarize(self, agent, context):
        return Task(
            description=f"{TASK_PROMPT}\nContext: {context}",
            expected_output=OUTPUT_FORMAT,
            agent=agent
        )
