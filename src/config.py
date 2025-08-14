"""
Configuration settings for the Intelligent Engine Maintenance Assistant.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Google AI Studio Configuration
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    gemini_model: str = Field("gemini-pro", env="GEMINI_MODEL")
    embedding_model: str = Field("models/embedding-001", env="EMBEDDING_MODEL")
    
    # Vector Database Configuration
    chroma_persist_directory: str = Field("./data/chroma_db", env="CHROMA_PERSIST_DIRECTORY")
    chroma_collection_name: str = Field("maintenance_docs", env="CHROMA_COLLECTION_NAME")
    
    # Application Configuration
    streamlit_port: int = Field(8501, env="STREAMLIT_PORT")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    max_query_length: int = Field(500, env="MAX_QUERY_LENGTH")
    max_results: int = Field(10, env="MAX_RESULTS")
    
    # RAG Configuration
    chunk_size: int = Field(1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    similarity_threshold: float = Field(0.7, env="SIMILARITY_THRESHOLD")
    max_context_length: int = Field(4000, env="MAX_CONTEXT_LENGTH")
    
    # Data Paths
    data_dir: str = Field("./data", env="DATA_DIR")
    raw_data_dir: str = Field("./data/raw", env="RAW_DATA_DIR")
    processed_data_dir: str = Field("./data/processed", env="PROCESSED_DATA_DIR")
    synthetic_data_dir: str = Field("./data/synthetic", env="SYNTHETIC_DATA_DIR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
