"""
Embeddings generation using Google AI Studio API.
"""
import time
import numpy as np
from typing import List, Optional, Dict, Any
from langchain.embeddings.base import Embeddings
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logging_config import get_logger
from src.config import settings

logger = get_logger(__name__)


class GoogleEmbeddings(Embeddings):
    """Google AI Studio embeddings implementation."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize Google embeddings.
        
        Args:
            api_key: Google AI Studio API key
            model: Embedding model name
        """
        self.api_key = api_key or settings.google_api_key
        self.model = model or settings.embedding_model
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        logger.info(f"Initialized Google embeddings with model: {self.model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents.
        
        Args:
            texts: List of text documents to embed
            
        Returns:
            List of embeddings for each document
        """
        embeddings = []
        
        for i, text in enumerate(texts):
            try:
                # Truncate text if too long
                if len(text) > 2048:
                    text = text[:2048]
                
                # Generate embedding
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                
                embeddings.append(result['embedding'])
                
                # Rate limiting - small delay between requests
                if i > 0 and i % 10 == 0:
                    time.sleep(1)
                    logger.debug(f"Processed {i+1}/{len(texts)} embeddings")
                    
            except Exception as e:
                logger.error(f"Error generating embedding for document {i}: {e}")
                # Return zero vector as fallback
                embeddings.append([0.0] * 768)  # Default dimension
        
        logger.info(f"Generated embeddings for {len(texts)} documents")
        return embeddings
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector for the query
        """
        try:
            # Truncate text if too long
            if len(text) > 2048:
                text = text[:2048]
            
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_query"
            )
            
            return result['embedding']
            
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 768


class EmbeddingManager:
    """Manages embedding operations and caching."""
    
    def __init__(self, embedding_model: GoogleEmbeddings = None):
        """Initialize embedding manager.
        
        Args:
            embedding_model: Embedding model instance
        """
        self.embedding_model = embedding_model or GoogleEmbeddings()
        self.cache: Dict[str, List[float]] = {}
    
    def get_embeddings(self, texts: List[str], use_cache: bool = True) -> List[List[float]]:
        """Get embeddings with optional caching.
        
        Args:
            texts: List of texts to embed
            use_cache: Whether to use caching
            
        Returns:
            List of embedding vectors
        """
        if not use_cache:
            return self.embedding_model.embed_documents(texts)
        
        embeddings = []
        texts_to_embed = []
        indices_to_embed = []
        
        # Check cache first
        for i, text in enumerate(texts):
            cache_key = self._get_cache_key(text)
            if cache_key in self.cache:
                embeddings.append(self.cache[cache_key])
            else:
                embeddings.append(None)
                texts_to_embed.append(text)
                indices_to_embed.append(i)
        
        # Generate embeddings for uncached texts
        if texts_to_embed:
            new_embeddings = self.embedding_model.embed_documents(texts_to_embed)
            
            # Update cache and results
            for idx, new_embedding in zip(indices_to_embed, new_embeddings):
                cache_key = self._get_cache_key(texts[idx])
                self.cache[cache_key] = new_embedding
                embeddings[idx] = new_embedding
        
        return embeddings
    
    def get_query_embedding(self, query: str, use_cache: bool = True) -> List[float]:
        """Get embedding for a query.
        
        Args:
            query: Query text
            use_cache: Whether to use caching
            
        Returns:
            Query embedding vector
        """
        if not use_cache:
            return self.embedding_model.embed_query(query)
        
        cache_key = self._get_cache_key(query)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        embedding = self.embedding_model.embed_query(query)
        self.cache[cache_key] = embedding
        return embedding
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return f"embed_{hash(text)}"
    
    def clear_cache(self):
        """Clear embedding cache."""
        self.cache.clear()
        logger.info("Embedding cache cleared")
    
    def cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "cached_embeddings": len(self.cache),
            "total_cache_size": sum(len(emb) for emb in self.cache.values())
        }
