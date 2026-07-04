from .document_processor import DocumentProcessor
from .embedding_service import EmbeddingService
from .retriever import Retriever

class KnowledgeManager:
    def __init__(self):
        self.processor = DocumentProcessor()
        self.embedder = EmbeddingService()
        self.retriever = Retriever()

    def ingest_document(self, business_id: str, content: bytes, filename: str):
        # 1. Parse and chunk (PDF, DOCX, TXT)
        chunks = self.processor.process(content, filename)
        # 2. Embed and store in ChromaDB
        self.embedder.store_embeddings(business_id, chunks)
        return True

    def retrieve(self, business_id: str, query: str):
        return self.retriever.search(business_id, query)
