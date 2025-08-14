#!/usr/bin/env python3
"""
Initialize the vector database with documents and synthetic data.
"""
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import settings
from src.utils.logging_config import setup_logging, get_logger
from src.data_processing.document_loader import DocumentProcessor
from src.rag_pipeline.pipeline import VectorStore

def main():
    """Initialize the database with all available documents."""

    # Setup logging
    setup_logging(settings.log_level)
    logger = get_logger(__name__)

    logger.info("Starting database initialization...")

    try:
        # Create necessary directories
        os.makedirs(settings.data_dir, exist_ok=True)
        os.makedirs(settings.raw_data_dir, exist_ok=True)
        os.makedirs(settings.processed_data_dir, exist_ok=True)
        os.makedirs(settings.synthetic_data_dir, exist_ok=True)
        os.makedirs(settings.chroma_persist_directory, exist_ok=True)

        # Initialize document processor
        doc_processor = DocumentProcessor()

        # Load all documents
        logger.info("Loading documents...")
        documents = doc_processor.load_all_documents()

        if not documents:
            logger.warning("No documents found. Make sure data files exist in the correct directories.")
            print("\n⚠️  No documents found!")
            print("Make sure these files exist:")
            print("- synthetic_maintenance_logs.csv")
            print("- synthetic_fleet_info.csv") 
            print("- synthetic_obd_codes.csv")
            return

        # Initialize vector store
        logger.info("Initializing vector store...")
        vector_store = VectorStore()

        # Add documents to vector store
        logger.info(f"Adding {len(documents)} documents to vector store...")
        vector_store.add_documents(documents)

        # Get collection info
        info = vector_store.get_collection_info()
        logger.info(f"Database initialized successfully!")
        logger.info(f"Collection: {info.get('name', 'unknown')}")
        logger.info(f"Document count: {info.get('count', 0)}")

        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE")
        print("="*50)
        print(f"Documents loaded: {len(documents)}")
        print(f"Collection name: {info.get('name', 'unknown')}")
        print(f"Persist directory: {settings.chroma_persist_directory}")
        print("\nYou can now run the Streamlit app:")
        print("streamlit run src/streamlit_app.py")
        print("="*50)

    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        print(f"\nError: {e}")
        print("Please check the logs for more details.")
        print("\nCommon issues:")
        print("1. Missing Google AI Studio API key in .env file")
        print("2. Missing synthetic data CSV files")
        print("3. Network connectivity issues")
        sys.exit(1)


if __name__ == "__main__":
    main()
