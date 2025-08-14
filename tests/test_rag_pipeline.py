"""
Tests for the RAG pipeline components.
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.rag_pipeline.pipeline import RAGPipeline, VectorStore, GoogleLLM
from src.data_processing.embeddings import GoogleEmbeddings
from src.data_processing.document_loader import DocumentProcessor


class TestGoogleEmbeddings(unittest.TestCase):
    """Test Google embeddings functionality."""

    def setUp(self):
        self.mock_api_key = "test_api_key"

    @patch('google.generativeai.configure')
    @patch('google.generativeai.embed_content')
    def test_embed_query(self, mock_embed, mock_configure):
        """Test query embedding generation."""
        # Mock response
        mock_embed.return_value = {'embedding': [0.1, 0.2, 0.3]}

        embeddings = GoogleEmbeddings(api_key=self.mock_api_key)
        result = embeddings.embed_query("test query")

        self.assertEqual(result, [0.1, 0.2, 0.3])
        mock_embed.assert_called_once()

    @patch('google.generativeai.configure')
    @patch('google.generativeai.embed_content')
    def test_embed_documents(self, mock_embed, mock_configure):
        """Test document embedding generation."""
        # Mock response
        mock_embed.return_value = {'embedding': [0.1, 0.2, 0.3]}

        embeddings = GoogleEmbeddings(api_key=self.mock_api_key)
        result = embeddings.embed_documents(["doc1", "doc2"])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [0.1, 0.2, 0.3])


class TestGoogleLLM(unittest.TestCase):
    """Test Google LLM functionality."""

    def setUp(self):
        self.mock_api_key = "test_api_key"

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_generate(self, mock_model_class, mock_configure):
        """Test text generation."""
        # Mock model instance
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Generated response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        llm = GoogleLLM(api_key=self.mock_api_key)
        result = llm.generate("test prompt")

        self.assertEqual(result, "Generated response")
        mock_model.generate_content.assert_called_once()


class TestDocumentProcessor(unittest.TestCase):
    """Test document processing functionality."""

    def setUp(self):
        self.processor = DocumentProcessor()

    def test_chunk_size_configuration(self):
        """Test chunk size is properly configured."""
        self.assertEqual(self.processor.chunk_size, 1000)
        self.assertEqual(self.processor.chunk_overlap, 200)

    def test_load_csv_data_empty_file(self):
        """Test loading from non-existent CSV file."""
        result = self.processor.load_csv_data("nonexistent.csv")
        self.assertEqual(result, [])


class TestRAGPipeline(unittest.TestCase):
    """Test RAG pipeline integration."""

    def setUp(self):
        self.mock_vector_store = Mock()
        self.mock_llm = Mock()
        self.pipeline = RAGPipeline(
            vector_store=self.mock_vector_store,
            llm=self.mock_llm
        )

    def test_query_no_documents(self):
        """Test query when no documents are found."""
        self.mock_vector_store.similarity_search.return_value = []

        result = self.pipeline.query("test question")

        self.assertIn("couldn't find relevant information", result["answer"].lower())
        self.assertEqual(result["confidence"], 0.0)
        self.assertEqual(result["sources"], [])

    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        from langchain.schema import Document

        # Mock retrieved documents
        retrieved_docs = [
            (Document(page_content="content1"), 0.8),
            (Document(page_content="content2"), 0.6)
        ]

        confidence = self.pipeline._calculate_confidence(retrieved_docs)
        expected_confidence = (0.8 + 0.6) / 2

        self.assertEqual(confidence, expected_confidence)


if __name__ == "__main__":
    unittest.main()
