from crewai import Task
from ai.prompts.marketing_prompt import TASK_PROMPT as MKT_PROMPT, OUTPUT_FORMAT as MKT_OUT
from ai.prompts.sales_prompt import TASK_PROMPT as SALES_PROMPT, OUTPUT_FORMAT as SALES_OUT
from ai.prompts.finance_prompt import TASK_PROMPT as FIN_PROMPT, OUTPUT_FORMAT as FIN_OUT
from ai.prompts.operations_prompt import TASK_PROMPT as OPS_PROMPT, OUTPUT_FORMAT as OPS_OUT
from ai.prompts.customer_success_prompt import TASK_PROMPT as CS_PROMPT, OUTPUT_FORMAT as CS_OUT

class ExecutionTasks:
    def plan_marketing_campaign(self, agent, context):
        return Task(
            description=f"{MKT_PROMPT}\nContext: {context}",
            expected_output=MKT_OUT,
            agent=agent
        )
    
    def plan_sales_pipeline(self, agent, context):
        return Task(
            description=f"{SALES_PROMPT}\nContext: {context}",
            expected_output=SALES_OUT,
            agent=agent
        )

    def review_budget(self, agent, context):
        return Task(
            description=f"{FIN_PROMPT}\nContext: {context}",
            expected_output=FIN_OUT,
            agent=agent
        )
        
    def assess_operations(self, agent, context):
        return Task(
            description=f"{OPS_PROMPT}\nContext: {context}",
            expected_output=OPS_OUT,
            agent=agent
        )

    def assess_customer_success(self, agent, context):
        return Task(
            description=f"{CS_PROMPT}\nContext: {context}",
            expected_output=CS_OUT,
            agent=agent
        )
