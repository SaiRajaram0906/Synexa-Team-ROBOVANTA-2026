from crewai.tools import BaseTool

class DocumentSearchTool(BaseTool):
    name: str = "Document Search"
    description: str = "Searches the business knowledge base (ChromaDB) for specific document contexts."

    def _run(self, query: str) -> str:
        # TODO: Call knowledge manager retriever
        return "TODO: Document Context"
