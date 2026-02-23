"""Vector storage and retrieval with ChromaDB"""
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        # Using sentence-transformers model (runs locally, no API needed)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
    def store_findings(
        self, 
        docs: List[Document], 
        collection_name: str = "research"
    ) -> Chroma:
        """Store documents in vector database"""
        try:
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                client=self.client,
                collection_name=collection_name,
                persist_directory=self.persist_directory
            )
            logger.info(f"Stored {len(docs)} documents in collection '{collection_name}'")
            return vectorstore
            
        except Exception as e:
            logger.error(f"Failed to store documents: {e}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 5,
        collection_name: str = "research",
        filter_metadata: Optional[dict] = None
    ) -> List[Document]:
        """Search for similar documents"""
        try:
            vectorstore = Chroma(
                client=self.client,
                collection_name=collection_name,
                embedding_function=self.embeddings
            )
            
            results = vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter_metadata
            )
            
            logger.info(f"Retrieved {len(results)} similar documents for '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []
    
    def get_retriever(self, k: int = 5, collection_name: str = "research"):
        """Get LangChain retriever interface"""
        vectorstore = Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
        return vectorstore.as_retriever(search_kwargs={"k": k})
