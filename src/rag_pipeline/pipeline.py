"""
RAG pipeline implementation with Google AI Studio integration.
"""
from typing import List, Dict, Any, Optional, Tuple
import google.generativeai as genai
from langchain.schema import Document
from langchain.vectorstores import Chroma
from tenacity import retry, stop_after_attempt, wait_exponential
from src.data_processing.embeddings import GoogleEmbeddings, EmbeddingManager
from src.utils.logging_config import get_logger
from src.config import settings

logger = get_logger(__name__)


class GoogleLLM:
    """Google Gemini LLM wrapper."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize Google LLM.
        
        Args:
            api_key: Google AI Studio API key
            model: Model name (e.g., 'gemini-pro')
        """
        self.api_key = api_key or settings.google_api_key
        self.model = model or settings.gemini_model
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
        logger.info(f"Initialized Google LLM with model: {self.model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text response.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.1,
                    top_p=0.8,
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error processing your request. Please try again."


class VectorStore:
    """Vector store wrapper using Chroma."""
    
    def __init__(self, collection_name: str = None, persist_directory: str = None):
        """Initialize vector store.
        
        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist data
        """
        self.collection_name = collection_name or settings.chroma_collection_name
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        self.embedding_manager = EmbeddingManager()
        
        # Initialize Chroma
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize or load the vector store."""
        try:
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_manager.embedding_model,
                persist_directory=self.persist_directory
            )
            logger.info(f"Initialized vector store: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        try:
            if not documents:
                logger.warning("No documents to add")
                return
            
            # Add documents in batches to avoid memory issues
            batch_size = 50
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                self.vectorstore.add_documents(batch)
                logger.info(f"Added batch {i//batch_size + 1}: {len(batch)} documents")
            
            # Persist the changes
            self.vectorstore.persist()
            logger.info(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 5, 
        threshold: float = None
    ) -> List[Tuple[Document, float]]:
        """Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            threshold: Similarity threshold
            
        Returns:
            List of (document, score) tuples
        """
        try:
            threshold = threshold or settings.similarity_threshold
            
            # Perform similarity search with scores
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Filter by threshold if specified
            if threshold:
                results = [(doc, score) for doc, score in results if score >= threshold]
            
            logger.info(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            collection = self.vectorstore._collection
            return {
                "name": self.collection_name,
                "count": collection.count(),
                "metadata": collection.metadata
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}


class RAGPipeline:
    """Complete RAG pipeline implementation."""
    
    def __init__(
        self,
        vector_store: VectorStore = None,
        llm: GoogleLLM = None,
        max_context_length: int = None
    ):
        """Initialize RAG pipeline.
        
        Args:
            vector_store: Vector store instance
            llm: Language model instance
            max_context_length: Maximum context length
        """
        self.vector_store = vector_store or VectorStore()
        self.llm = llm or GoogleLLM()
        self.max_context_length = max_context_length or settings.max_context_length
        
        logger.info("Initialized RAG pipeline")
    
    def query(
        self, 
        question: str, 
        k: int = 5,
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """Process a query through the RAG pipeline.
        
        Args:
            question: User question
            k: Number of documents to retrieve
            include_sources: Whether to include source documents
            
        Returns:
            Dictionary containing answer and metadata
        """
        try:
            # Retrieve relevant documents
            retrieved_docs = self.vector_store.similarity_search(question, k=k)
            
            if not retrieved_docs:
                return {
                    "answer": "I couldn't find relevant information to answer your question. Please try rephrasing or asking about a different topic.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Prepare context from retrieved documents
            context = self._prepare_context(retrieved_docs)
            
            # Generate answer
            answer = self._generate_answer(question, context)
            
            # Prepare response
            response = {
                "answer": answer,
                "confidence": self._calculate_confidence(retrieved_docs),
                "sources": []
            }
            
            if include_sources:
                response["sources"] = self._format_sources(retrieved_docs)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "sources": [],
                "confidence": 0.0
            }
    
    def _prepare_context(self, retrieved_docs: List[Tuple[Document, float]]) -> str:
        """Prepare context from retrieved documents.
        
        Args:
            retrieved_docs: List of (document, score) tuples
            
        Returns:
            Formatted context string
        """
        context_parts = []
        current_length = 0
        
        for doc, score in retrieved_docs:
            doc_text = doc.page_content
            
            # Check if adding this document would exceed max context length
            if current_length + len(doc_text) > self.max_context_length:
                # Truncate the document to fit
                remaining_length = self.max_context_length - current_length
                if remaining_length > 100:  # Only add if meaningful content can fit
                    doc_text = doc_text[:remaining_length] + "..."
                    context_parts.append(f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc_text}")
                break
            
            context_parts.append(f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc_text}")
            current_length += len(doc_text)
        
        return "\n\n".join(context_parts)
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using the LLM.
        
        Args:
            question: User question
            context: Context from retrieved documents
            
        Returns:
            Generated answer
        """
        prompt = f"""You are an expert maintenance advisor for commercial trucking fleets. Use the provided context to answer the user's question accurately and helpfully.

Context:
{context}

Question: {question}

Instructions:
- Provide a detailed, practical answer based on the context
- Focus on actionable maintenance advice
- Include specific procedures, costs, or timeframes when available
- If the question relates to safety or compliance, emphasize those aspects
- If the context doesn't contain enough information, say so clearly
- Cite sources when referencing specific information

Answer:"""

        return self.llm.generate(prompt, max_tokens=1000)
    
    def _calculate_confidence(self, retrieved_docs: List[Tuple[Document, float]]) -> float:
        """Calculate confidence score based on retrieval results.
        
        Args:
            retrieved_docs: List of (document, score) tuples
            
        Returns:
            Confidence score between 0 and 1
        """
        if not retrieved_docs:
            return 0.0
        
        # Use average similarity score as confidence
        avg_score = sum(score for _, score in retrieved_docs) / len(retrieved_docs)
        
        # Normalize to 0-1 range (assuming similarity scores are 0-1)
        confidence = min(1.0, max(0.0, avg_score))
        
        return round(confidence, 2)
    
    def _format_sources(self, retrieved_docs: List[Tuple[Document, float]]) -> List[Dict[str, Any]]:
        """Format source information for response.
        
        Args:
            retrieved_docs: List of (document, score) tuples
            
        Returns:
            List of formatted source dictionaries
        """
        sources = []
        
        for i, (doc, score) in enumerate(retrieved_docs):
            source_info = {
                "id": i + 1,
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": round(score, 3)
            }
            sources.append(source_info)
        
        return sources
