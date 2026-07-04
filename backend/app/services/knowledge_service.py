from ai.knowledge.knowledge_manager import KnowledgeManager

class KnowledgeService:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager()

    def process_and_store_document(self, business_id: str, document_content: bytes, filename: str):
        # TODO: Route document to processor, generate embeddings, store in ChromaDB
        return self.knowledge_manager.ingest_document(business_id, document_content, filename)
        
    def retrieve_context(self, business_id: str, query: str):
        return self.knowledge_manager.retrieve(business_id, query)
