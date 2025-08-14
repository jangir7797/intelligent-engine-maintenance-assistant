"""
Document loading and processing utilities.
"""
import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain.document_loaders import PyPDFDirectoryLoader, CSVLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.utils.logging_config import get_logger
from src.config import settings

logger = get_logger(__name__)


class DocumentProcessor:
    """Handles document loading, processing, and chunking."""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """Initialize the document processor.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
    def load_pdfs(self, directory_path: str) -> List[Document]:
        """Load PDF documents from a directory.
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            List of loaded documents
        """
        try:
            logger.info(f"Loading PDFs from {directory_path}")
            loader = PyPDFDirectoryLoader(directory_path)
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} PDF documents")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDFs: {e}")
            return []
    
    def load_csv_data(self, file_path: str) -> List[Document]:
        """Load CSV data and convert to documents.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of documents created from CSV rows
        """
        try:
            logger.info(f"Loading CSV data from {file_path}")
            df = pd.read_csv(file_path)
            documents = []
            
            for idx, row in df.iterrows():
                # Convert row to text representation
                content = "\n".join([f"{col}: {val}" for col, val in row.items()])
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": file_path,
                        "row_index": idx,
                        "type": "csv_data"
                    }
                )
                documents.append(doc)
            
            logger.info(f"Created {len(documents)} documents from CSV")
            return documents
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return []
    
    def load_maintenance_logs(self) -> List[Document]:
        """Load synthetic maintenance logs."""
        file_path = Path("synthetic_maintenance_logs.csv")
        if not file_path.exists():
            logger.warning(f"Maintenance logs not found at {file_path}")
            return []
            
        documents = self.load_csv_data(str(file_path))
        # Add specific metadata for maintenance logs
        for doc in documents:
            doc.metadata.update({"document_type": "maintenance_log"})
        return documents
    
    def load_fleet_info(self) -> List[Document]:
        """Load synthetic fleet information."""
        file_path = Path("synthetic_fleet_info.csv")
        if not file_path.exists():
            logger.warning(f"Fleet info not found at {file_path}")
            return []
            
        documents = self.load_csv_data(str(file_path))
        # Add specific metadata for fleet info
        for doc in documents:
            doc.metadata.update({"document_type": "fleet_info"})
        return documents
    
    def load_obd_codes(self) -> List[Document]:
        """Load synthetic OBD codes."""
        file_path = Path("synthetic_obd_codes.csv")
        if not file_path.exists():
            logger.warning(f"OBD codes not found at {file_path}")
            return []
            
        documents = self.load_csv_data(str(file_path))
        # Add specific metadata for OBD codes
        for doc in documents:
            doc.metadata.update({"document_type": "obd_codes"})
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of chunked documents
        """
        try:
            logger.info(f"Chunking {len(documents)} documents")
            chunked_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunked_docs)} chunks")
            return chunked_docs
        except Exception as e:
            logger.error(f"Error chunking documents: {e}")
            return documents
    
    def load_all_documents(self) -> List[Document]:
        """Load all available documents from various sources.
        
        Returns:
            List of all loaded and processed documents
        """
        all_documents = []
        
        # Load synthetic data
        maintenance_docs = self.load_maintenance_logs()
        fleet_docs = self.load_fleet_info()
        obd_docs = self.load_obd_codes()
        
        all_documents.extend(maintenance_docs)
        all_documents.extend(fleet_docs)
        all_documents.extend(obd_docs)
        
        # Add sample maintenance manual
        sample_manual = self.create_sample_manual()
        if sample_manual:
            all_documents.append(sample_manual)
        
        # Chunk all documents
        if all_documents:
            all_documents = self.chunk_documents(all_documents)
        
        logger.info(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def create_sample_manual(self) -> Optional[Document]:
        """Create a sample maintenance manual document."""
        manual_content = """
# Commercial Vehicle Engine Maintenance Manual

## Chapter 1: Engine Oil System

### Oil Change Procedures
Regular oil changes are critical for engine longevity. For commercial diesel engines:
- Change interval: Every 15,000-25,000 miles or 6 months
- Oil capacity: 10-15 gallons depending on engine size
- Recommended oil: 15W-40 heavy-duty diesel engine oil

### Oil Analysis
Monitor oil condition through regular analysis:
- Metal content indicates wear patterns
- Viscosity changes suggest contamination
- Acid number indicates oxidation levels

## Chapter 2: Cooling System Maintenance

### Coolant System Inspection
The cooling system prevents engine overheating:
- Check coolant level weekly
- Inspect hoses for cracks or leaks
- Test thermostat operation at 180-195°F
- Flush system every 100,000 miles

### Common Cooling Issues
- Overheating: Check radiator, water pump, thermostat
- Coolant loss: Inspect for external leaks
- Poor heating: May indicate low coolant or air pockets

## Chapter 3: Diagnostic Trouble Codes

### OBD-II System
The On-Board Diagnostic system monitors engine performance:
- P0171: System Too Lean (Bank 1) - Check for vacuum leaks, fuel pressure
- P0300: Random Misfire - Inspect spark plugs, fuel injectors, compression
- P0420: Catalyst Efficiency Below Threshold - Replace catalytic converter
- P2002: DPF Efficiency Below Threshold - Perform DPF regeneration

### DOT Compliance Requirements
Annual inspection items required by DOT:
- Brake system operation and adjustment
- Steering and suspension components
- Lighting and electrical systems
- Engine mounting and condition
- Exhaust system integrity

## Troubleshooting Guide

### Engine Won't Start
1. Check battery voltage (12.6V minimum)
2. Verify fuel supply and quality
3. Check air intake for restrictions
4. Test glow plugs (diesel engines)
5. Examine starter motor operation

### Engine Overheating
1. Check coolant level immediately
2. Inspect radiator for blockage
3. Test thermostat operation
4. Check water pump function
5. Verify fan operation

### Low Oil Pressure
1. Check oil level immediately
2. Verify oil viscosity is correct
3. Inspect oil pump operation
4. Check for internal engine wear
5. Replace oil pressure sensor

### Poor Fuel Economy
1. Check air filter restriction
2. Verify fuel quality
3. Test fuel injectors
4. Check tire pressure
5. Evaluate driving habits
"""
        
        return Document(
            page_content=manual_content,
            metadata={
                "source": "sample_maintenance_manual.txt",
                "document_type": "maintenance_manual",
                "type": "manual"
            }
        )
