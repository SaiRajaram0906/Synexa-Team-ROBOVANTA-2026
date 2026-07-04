from crewai.tools import BaseTool

class ReportGenerator(BaseTool):
    name: str = "Report Generator"
    description: str = "Compiles disparate agent outputs into a cohesive executive summary."

    def _run(self, agent_outputs: dict) -> str:
        # TODO: Generate markdown report
        return "TODO: Markdown Executive Summary"
